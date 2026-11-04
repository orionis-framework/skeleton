from orionis.mcp import McpResponse, Prompt, PromptArgument


class GreetingPrompt(Prompt):
    """Build a reusable greeting request for an MCP client."""

    name = "greeting"
    description = "Prepare a greeting request for a named person."
    arguments = (
        PromptArgument(name="name", description="Person to greet.", required=True),
        PromptArgument(name="style", description="Greeting style.", required=False),
    )

    async def handle(self, name: str, style: str = "friendly") -> McpResponse:
        """
        Construct a user message from the declared text arguments.

        Parameters
        ----------
        name : str
            Person supplied by the MCP client.
        style : str, optional
            Requested greeting style; defaults to ``friendly``.

        Returns
        -------
        McpResponse
            User-role prompt message for the client to use in a conversation.
        """
        return McpResponse.text(f"Greet {name} in a {style} way.").asUser()
