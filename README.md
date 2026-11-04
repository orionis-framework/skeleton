<p align="center">
  <img src="https://orionis-framework.com/favicon.svg" alt="Orionis Framework" width="180" />
</p>

<h1 align="center">Orionis Slim MCP Skeleton</h1>

<p align="center">Write Python. Build the whole application.</p>

<p align="center">
  <a href="https://docs.orionis-framework.com/">Documentation</a> &bull;
  <a href="https://api.orionis-framework.com/">API reference</a> &bull;
  <a href="https://orionis-framework.com/">Website</a>
</p>

This is the **minimal MCP application skeleton** from the `slim_mcp_1.x` branch. It registers an HTTP MCP server and the built-in health endpoint, with a service provider and exception handler. The framework implementation is installed as the `orionis` dependency.

## Requirements and setup

Use **Python 3.14+**, [uv](https://docs.astral.sh/uv/), and **Orionis 1.5 or later within 1.x**. `pyproject.toml` declares the supported framework range. The initial `uv sync` resolves dependencies and creates a local `uv.lock`; that generated file is not included in this template.

Run commands from this application's root. For a new checkout, copy `.env.example` to `.env` if `.env` does not already exist. Use `cp .env.example .env` on POSIX shells or `Copy-Item .env.example .env` in PowerShell. Keep an existing application's environment values and key.

```shell
uv sync
uv run orionis key:generate
```

`key:generate` stores a new `APP_KEY` in `.env` and preserves an existing key unless explicitly forced. The example sets `APP_URL` to `http://127.0.0.1:8000`, matching the development server. Adjust it to the application's base URL and review the selected services in `config/`. `.env.reference` documents additional configuration variables.

## Run and test

```shell
uv run orionis serve
uv run orionis test
uv run ruff check .
```

`serve` starts the development server; stop it before running other foreground commands in the same terminal. Inspect registered routes with `uv run orionis route:list` and available commands with `uv run orionis list`. The bundled `reactor` script remains an alternative, for example `uv run python -B reactor test`.

## Included MCP server

`app/mcp/servers/example.py` declares `ExampleServer` with one example of each capability. `routes/ai.py` exposes it at `/mcp` through `Mcp.web()`.

| Capability | Identifier | Behavior |
| --- | --- | --- |
| Tool | `echo` | Accepts a required string `message` and returns it unchanged. |
| Resource | `docs://example/guide` | Returns a fixed text guide without opening arbitrary files. |
| Prompt | `greeting` | Builds a user message from a required `name` and an optional `style`, which defaults to `friendly`. |

Open [Orionis MCP Inspector](https://inspector.orionis-framework.com/) after starting the application and connect to `http://127.0.0.1:8000/mcp`. Explore the catalogs, call `echo`, read the guide URI, and get `greeting` with `name="Ada"`. The HTTP and MCP configurations allow the Inspector's origin by default; leave `CORS_ALLOW_ORIGINS` unset for this setup. Override it with explicit origins when using another browser client.

The MCP directories are siblings: `app/mcp/tools/`, `app/mcp/resources/`, `app/mcp/prompts/`, and `app/mcp/servers/`. Add capabilities in the corresponding directory and register them in the server's tuples. They are not discovered merely by creating a file. `GET /up` is the health endpoint; `/` is not a predefined browser page.

After starting the server, discover the example over HTTP using the native MCP protocol:

```shell
curl --request POST \
  --url http://127.0.0.1:8000/mcp \
  --header 'Accept: application/json, text/event-stream' \
  --header 'Content-Type: application/json' \
  --header 'mcp-method: server/discover' \
  --header 'mcp-protocol-version: 2026-07-28' \
  --data '{"jsonrpc":"2.0","id":1,"method":"server/discover","params":{"_meta":{"io.modelcontextprotocol/protocolVersion":"2026-07-28","io.modelcontextprotocol/clientCapabilities":{},"io.modelcontextprotocol/clientInfo":{"name":"ExampleClient","version":"1.0.0"}}}}'
```

Invoke the included tool over HTTP:

```shell
curl --request POST \
  --url http://127.0.0.1:8000/mcp \
  --header 'Accept: application/json, text/event-stream' \
  --header 'Content-Type: application/json' \
  --header 'mcp-method: tools/call' \
  --header 'mcp-name: echo' \
  --header 'mcp-protocol-version: 2026-07-28' \
  --data '{"jsonrpc":"2.0","id":2,"method":"tools/call","params":{"name":"echo","arguments":{"message":"Hello Orionis"},"_meta":{"io.modelcontextprotocol/protocolVersion":"2026-07-28","io.modelcontextprotocol/clientCapabilities":{}}}}'
```

`tests/test_mcp.py` exercises all three catalogs, tool calls, resource reads, prompt messages, optional defaults, and rejected arguments through the framework's in-process MCP client. A prompt returns conversation messages; it does not invoke a language model.

To also expose this declaration over local STDIO, add a local registration beside `Mcp.web()` in `routes/ai.py`:

```python
Mcp.local("example", ExampleServer)
```

Then launch that registered local server with `uv run orionis mcp:start example`. The HTTP server continues to use `uv run orionis serve`. See the [MCP server guide](https://docs.orionis-framework.com/en/mcp/servers-and-routes) and [transport configuration](https://docs.orionis-framework.com/en/mcp/stdio-and-configuration) for typed tools, headers, origins, authentication, and STDIO integration.

This template does not register WEB, API, or console-route files. Add other runtime contexts explicitly in `bootstrap/app.py` when needed. Configure SQL-backed services and their [storage preparation commands](https://docs.orionis-framework.com/en/database/commands#internal-storage-commands) only if your application uses them.

## Configuration and application data

`config/app.py` sets application identity and runtime values; `http.py` exposes request limits, host/proxy policy, and HTTP CORS; `mcp.py` controls MCP origins and protocol budgets; `logging.py` and `testing.py` expose diagnostics and test discovery. `database.py` provides optional SQL connections for your own capabilities. There is no browser authentication or session configuration in this variant.

The examples do not require database tables. `database/migrations/`, `database/schemas/`, `database/factories/`, and `database/seeders/` contain only placeholders for application-owned data; `app/models/` is ready for future models. No migrations for framework storage are duplicated here. SQLite creates `database/database.sqlite` when an application SQL operation first opens it; database files and their journal sidecars are excluded from Git. An alternative database path needs an existing parent directory.

## Framework conventions

Class methods use `camelCase`, `_camelCase`, or `__camelCase`; functions outside classes use `snake_case`. Python protocol methods retain their required names, such as `__init__`. Document Python APIs with NumPy-style docstrings.

Schema validation remains strict outside the scope of an explicit `Coerce()` marker. Schemas support coercion before type, constraint, and rule checks, and the complementary `Empty()` and `NoEmpty()` rules. See [schema declarations](https://docs.orionis-framework.com/en/validation/declaring-schemas#field-coercion) and [empty-value rules](https://docs.orionis-framework.com/en/validation/application-rules#empty-and-no-empty) when defining application inputs. Query builders also support [`toSql()`](https://docs.orionis-framework.com/en/database/query-builder#api-tosql) for SQL inspection without executing a query.

## Project links

- [Framework source](https://github.com/orionis-framework/framework)
- [Skeleton variants](https://github.com/orionis-framework/skeleton)
- [Documentation](https://docs.orionis-framework.com/)
- [CLI installer](https://github.com/orionis-framework/installer)
- [Discussions](https://github.com/orgs/orionis-framework/discussions)
- [Support development](https://github.com/sponsors/rmunate)

Created and maintained by [Raul Mauricio Uñate Castro](https://github.com/rmunate). Released under the [MIT license](LICENCE).
