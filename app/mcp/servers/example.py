from orionis.mcp import Server
from app.mcp.prompts.greeting import GreetingPrompt
from app.mcp.resources.guide import GuideResource
from app.mcp.tools.echo import EchoTool

class ExampleServer(Server):
    """Expose application tools, resources and prompts through MCP."""

    name = "ExampleServer"
    version = "1.0.0"
    instructions = (
        "Call echo to return a message unchanged, read docs://example/guide "
        "for usage instructions, or request the greeting prompt."
    )

    tools = (EchoTool,)
    resources = (GuideResource,)
    prompts = (GreetingPrompt,)
