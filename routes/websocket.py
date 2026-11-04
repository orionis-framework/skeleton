from app.realtime.hubs.echo_hub import EchoHub
from app.realtime.sockets.echo_socket import EchoSocket
from orionis.support.facades import Route

Route.hub("/realtime/echo", EchoHub)
Route.websocket("/ws/echo", EchoSocket)
