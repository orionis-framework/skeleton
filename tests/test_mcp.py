from app.mcp.servers.example import ExampleServer
from orionis.test import TestCase

class TestMcp(TestCase):

    async def testEchoToolIsDiscoverable(self) -> None:
        """
        Expose the echo tool and its typed input through the MCP catalog.

        Returns
        -------
        None
            Verify the published tool name and required string argument.
        """
        client = await self.mcp(ExampleServer)
        response = await client.request("tools/list")
        response.assertOk()
        tools = response.message["result"]["tools"]
        self.assertEqual([tool["name"] for tool in tools], ["echo"])
        schema = tools[0]["inputSchema"]
        self.assertEqual(schema["properties"]["message"]["type"], "string")
        self.assertIn("message", schema["required"])

    async def testEchoToolReturnsMessage(self) -> None:
        """
        Preserve text across a serialized MCP tool call.

        Returns
        -------
        None
            Verify that whitespace and Unicode survive the protocol round trip.
        """
        client = await self.mcp(ExampleServer)
        message = "  Hola, Orión!\n"
        response = await client.tool("echo", {"message": message})
        response.assertOk()
        self.assertEqual(
            response.message["result"]["content"],
            [{"type": "text", "text": message}],
        )

    async def testEchoToolRejectsInvalidArguments(self) -> None:
        """
        Reject missing or incorrectly typed messages through MCP validation.

        Returns
        -------
        None
            Verify that invalid inputs become tool errors without coercion.
        """
        client = await self.mcp(ExampleServer)
        for arguments in ({}, {"message": 12}, {"message": None}):
            with self.subTest(arguments=arguments):
                response = await client.tool("echo", arguments)
                self.assertTrue(response.message["result"]["isError"])
                response.assertTextContains("Invalid tool arguments")

    async def testGuideResourceCanBeListedAndRead(self) -> None:
        """
        Discover the guide and read its content through the registered URI.

        Returns
        -------
        None
            Verify resource identity, MIME type, and serialized text content.
        """
        client = await self.mcp(ExampleServer)
        catalog = await client.request("resources/list")
        catalog.assertOk()
        resources = catalog.message["result"]["resources"]
        self.assertEqual([resource["name"] for resource in resources], ["guide"])
        self.assertEqual(resources[0]["uri"], "docs://example/guide")

        response = await client.request(
            "resources/read", {"uri": resources[0]["uri"]},
        )
        response.assertOk()
        contents = response.message["result"]["contents"]
        self.assertEqual(len(contents), 1)
        self.assertEqual(contents[0]["uri"], "docs://example/guide")
        self.assertEqual(contents[0]["mimeType"], "text/plain")
        self.assertIn("Call echo with a message", contents[0]["text"])

    async def testUnregisteredResourceIsRejected(self) -> None:
        """
        Reject a URI that the server has not registered.

        Returns
        -------
        None
            Verify that arbitrary resource paths do not return application data.
        """
        client = await self.mcp(ExampleServer)
        response = await client.request(
            "resources/read", {"uri": "docs://example/missing"},
        )
        self.assertEqual(response.message["error"]["code"], -32602)
        self.assertNotIn("result", response.message)

    async def testGreetingPromptDeclaresItsArguments(self) -> None:
        """
        Publish the greeting prompt with required and optional text arguments.

        Returns
        -------
        None
            Verify the prompt catalog describes the arguments clients may send.
        """
        client = await self.mcp(ExampleServer)
        response = await client.request("prompts/list")
        response.assertOk()
        prompts = response.message["result"]["prompts"]
        self.assertEqual([prompt["name"] for prompt in prompts], ["greeting"])
        arguments = {
            argument["name"]: argument for argument in prompts[0]["arguments"]
        }
        self.assertTrue(arguments["name"]["required"])
        self.assertFalse(arguments["style"].get("required", False))

    async def testGreetingPromptUsesDefaultAndExplicitStyle(self) -> None:
        """
        Preserve user roles and resolve optional prompt arguments.

        Returns
        -------
        None
            Verify generated messages with the default and a supplied style.
        """
        client = await self.mcp(ExampleServer)
        cases = (
            ({"name": "Ada"}, "Greet Ada in a friendly way."),
            ({"name": "Ada", "style": "formal"}, "Greet Ada in a formal way."),
        )
        for arguments, expected in cases:
            with self.subTest(arguments=arguments):
                response = await client.request(
                    "prompts/get", {"name": "greeting", "arguments": arguments},
                )
                response.assertOk()
                self.assertEqual(
                    response.message["result"]["messages"],
                    [{"role": "user", "content": {"type": "text", "text": expected}}],
                )

    async def testGreetingPromptRejectsInvalidArguments(self) -> None:
        """
        Reject absent, unknown, or nontext prompt arguments.

        Returns
        -------
        None
            Verify invalid prompt arguments produce protocol parameter errors.
        """
        client = await self.mcp(ExampleServer)
        cases = (
            {},
            {"name": 12},
            {"name": "Ada", "style": None},
            {"name": "Ada", "unexpected": "value"},
        )
        for arguments in cases:
            with self.subTest(arguments=arguments):
                response = await client.request(
                    "prompts/get", {"name": "greeting", "arguments": arguments},
                )
                self.assertEqual(response.message["error"]["code"], -32602)
