from orionis.mcp import McpResponse, Resource


class GuideResource(Resource):
    """Expose a fixed guide without opening client-supplied filesystem paths."""

    name = "guide"
    uri = "docs://example/guide"
    description = "Read the guide to this server's example capabilities."
    mime_type = "text/plain"

    async def handle(self) -> McpResponse:
        """
        Return the server's example usage guide as a text resource.

        Returns
        -------
        McpResponse
            Text content identified by the registered resource URI.
        """
        return McpResponse.resource(
            self.uri,
            "Call echo with a message to return it unchanged. "
            "Request the greeting prompt with a name and an optional style.",
            self.mime_type,
        )
