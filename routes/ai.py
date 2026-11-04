from app.mcp.servers.example import ExampleServer
from orionis.support.facades import Mcp

Mcp.web("/mcp", ExampleServer)

# Start the application with `uv run orionis serve`, then open the MCP Inspector:
# https://inspector.orionis-framework.com/
# Connect it to http://127.0.0.1:8000/mcp to explore the tool, resource, and prompt.
# The default HTTP and MCP origin allowlists already include this Inspector.
