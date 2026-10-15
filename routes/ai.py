from app.mcp.servers.example import ExampleServer
from orionis.support.facades import Mcp

Mcp.web("/mcp", ExampleServer)

# Example curl command to test the MCP server endpoint.
# curl --request POST \
#   --url http://localhost:8000/mcp \
#   --header 'Accept: application/json, text/event-stream' \
#   --header 'Content-Type: application/json' \
#   --header 'mcp-method: server/discover' \
#   --header 'mcp-protocol-version: 2026-07-28' \
#   --data '{"jsonrpc":"2.0","id":1,"method":"server/discover","params":{"_meta":{"io.modelcontextprotocol/protocolVersion":"2026-07-28","io.modelcontextprotocol/clientCapabilities":{},"io.modelcontextprotocol/clientInfo":{"name":"StatusServer","version":"1.0.0"}}}}'
