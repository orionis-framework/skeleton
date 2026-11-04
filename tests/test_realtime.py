import asyncio
from contextlib import asynccontextmanager
import json
from typing import TYPE_CHECKING
from orionis.foundation.contracts.application import IApplication
from orionis.realtime.contracts.manager import IConnectionManager
from orionis.test import TestCase

if TYPE_CHECKING:
    from collections.abc import AsyncIterator

class WebSocketPeer:
    """Drive the application's ASGI interface without opening a network port."""

    def __init__(
        self,
        path: str,
        origin: str = "http://127.0.0.1:8000",
    ) -> None:
        """
        Prepare a connection event and independent input and output queues.

        Parameters
        ----------
        path : str
            Registered WebSocket endpoint to exercise.
        origin : str, optional
            Browser origin included in the handshake.

        Returns
        -------
        None
            Store the ASGI scope and queue the initial connection event.
        """
        self.scope = {
            "type": "websocket",
            "asgi": {"version": "3.0", "spec_version": "2.5"},
            "http_version": "1.1",
            "scheme": "ws",
            "path": path,
            "raw_path": path.encode(),
            "query_string": b"",
            "root_path": "",
            "headers": [
                (b"host", b"127.0.0.1:8000"),
                (b"origin", origin.encode()),
            ],
            "server": ("127.0.0.1", 8000),
            "client": ("127.0.0.1", 50000),
            "subprotocols": [],
            "state": {},
        }
        self.events: asyncio.Queue[dict] = asyncio.Queue()
        self.output: asyncio.Queue[dict] = asyncio.Queue()
        self.events.put_nowait({"type": "websocket.connect"})

    @asynccontextmanager
    async def connection(self, app: IApplication) -> AsyncIterator[WebSocketPeer]:
        """
        Run the connection and await its cleanup after disconnection.

        Parameters
        ----------
        app : IApplication
            Booted application supplied by the test runner.

        Yields
        ------
        WebSocketPeer
            Peer connected to the application's native ASGI handler.
        """
        owner = asyncio.create_task(
            app(self.scope, self.events.get, self.output.put),
        )
        try:
            yield self
        finally:
            self.events.put_nowait({
                "type": "websocket.disconnect", "code": 1000,
            })
            try:
                await asyncio.wait_for(owner, timeout=2)
            finally:
                owner.cancel()
                await asyncio.gather(owner, return_exceptions=True)

    def sendText(self, text: str) -> None:
        """
        Queue one client text frame.

        Parameters
        ----------
        text : str
            Payload delivered to the application's receive callback.

        Returns
        -------
        None
            Enqueue the frame without executing the handler directly.
        """
        self.events.put_nowait({"type": "websocket.receive", "text": text})

    async def nextEvent(self) -> dict:
        """
        Receive the next server frame within a bounded timeout.

        Returns
        -------
        dict
            ASGI event emitted by the application's send callback.
        """
        return await asyncio.wait_for(self.output.get(), timeout=2)

class TestRealtime(TestCase):

    async def testRawSocketEchoesText(self, app: IApplication) -> None:
        """
        Accept a same-origin connection and preserve its text payload.

        Parameters
        ----------
        app : IApplication
            Booted application supplied by the test runner.

        Returns
        -------
        None
            Verify raw echo behavior and orderly peer disconnection.
        """
        peer = WebSocketPeer("/ws/echo")
        async with peer.connection(app):
            self.assertEqual((await peer.nextEvent())["type"], "websocket.accept")
            message = "  Hola, Orión!\n"
            peer.sendText(message)
            frame = await peer.nextEvent()
            self.assertEqual(frame["type"], "websocket.send")
            self.assertEqual(frame["text"], message)

    async def testHubEchoesMessageAndReleasesConnection(
        self,
        app: IApplication,
    ) -> None:
        """
        Complete an RPC invocation and release its connection on disconnect.

        Parameters
        ----------
        app : IApplication
            Booted application supplied by the test runner.

        Returns
        -------
        None
            Verify ready metadata, correlated completion and connection cleanup.
        """
        peer = WebSocketPeer("/realtime/echo")
        async with peer.connection(app):
            self.assertEqual((await peer.nextEvent())["type"], "websocket.accept")
            ready = json.loads((await peer.nextEvent())["text"])
            self.assertEqual(ready["type"], "ready")
            self.assertEqual(ready["version"], 1)
            self.assertTrue(ready["connection_id"])
            peer.sendText(json.dumps({
                "type": "invoke", "id": "echo-1", "target": "echo",
                "args": ["Hello Orionis"],
            }))
            completion = json.loads((await peer.nextEvent())["text"])
            self.assertEqual(completion, {
                "type": "completion", "id": "echo-1", "result": "Hello Orionis",
            })
        manager = await app.make(IConnectionManager)
        self.assertEqual(manager.snapshot(), ())

    async def testHubRejectsMalformedPayload(self, app: IApplication) -> None:
        """
        Close malformed RPC input with the protocol-error close code.

        Parameters
        ----------
        app : IApplication
            Booted application supplied by the test runner.

        Returns
        -------
        None
            Verify invalid JSON closes the connection without a completion.
        """
        peer = WebSocketPeer("/realtime/echo")
        async with peer.connection(app):
            self.assertEqual((await peer.nextEvent())["type"], "websocket.accept")
            self.assertEqual(
                json.loads((await peer.nextEvent())["text"])["type"], "ready",
            )
            peer.sendText("not-json")
            close = await peer.nextEvent()
            self.assertEqual(close["type"], "websocket.close")
            self.assertEqual(close["code"], 1002)

    async def testHubExposesOnlyRemoteMethods(self, app: IApplication) -> None:
        """
        Reject calls to an unregistered lifecycle method.

        Parameters
        ----------
        app : IApplication
            Booted application supplied by the test runner.

        Returns
        -------
        None
            Verify that only explicitly remote methods are callable by clients.
        """
        peer = WebSocketPeer("/realtime/echo")
        async with peer.connection(app):
            self.assertEqual((await peer.nextEvent())["type"], "websocket.accept")
            await peer.nextEvent()
            peer.sendText(json.dumps({
                "type": "invoke", "id": "private-1", "target": "onConnect",
            }))
            response = json.loads((await peer.nextEvent())["text"])
            self.assertEqual(response["id"], "private-1")
            self.assertEqual(response["error"]["code"], "method_not_found")

    async def testForeignOriginsAreRejected(self, app: IApplication) -> None:
        """
        Reject foreign browser origins before either endpoint accepts them.

        Parameters
        ----------
        app : IApplication
            Booted application supplied by the test runner.

        Returns
        -------
        None
            Verify both the raw socket and Hub enforce the default origin policy.
        """
        for path in ("/ws/echo", "/realtime/echo"):
            with self.subTest(path=path):
                peer = WebSocketPeer(path, origin="https://untrusted.example")
                async with peer.connection(app):
                    rejection = await peer.nextEvent()
                    self.assertEqual(rejection["type"], "websocket.close")
                    self.assertEqual(rejection["code"], 1008)
