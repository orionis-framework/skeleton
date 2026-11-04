from orionis.mcp import McpResponse, Tool
from orionis.schemas import Schema

class EchoInput(Schema):
    """
    Declare the arguments accepted by the echo tool.

    Attributes
    ----------
    message : str
        Message to return without modifying its contents.
    """

    message: str

class EchoTool(Tool[EchoInput]):
    """Return a client message through a typed MCP tool."""

    name = "echo"
    description = "Return the supplied message without modifying it."
    input = EchoInput

    async def handle(self, payload: EchoInput) -> McpResponse:
        """
        Return the validated message as MCP text content.

        Parameters
        ----------
        payload : EchoInput
            Validated arguments supplied by the MCP client.

        Returns
        -------
        McpResponse
            Text response containing the original message.
        """
        return McpResponse.text(payload.message)
