<p align="center">
  <img src="https://orionis-framework.com/favicon.svg" alt="Orionis Framework" width="180" />
</p>

<h1 align="center">Orionis Blank Skeleton</h1>

<p align="center">Write Python. Build the whole application.</p>

<p align="center">
  <a href="https://docs.orionis-framework.com/">Documentation</a> &bull;
  <a href="https://api.orionis-framework.com/">API reference</a> &bull;
  <a href="https://orionis-framework.com/">Website</a>
</p>

This is the **blank application skeleton** from the `blank_1.x` branch. It registers empty HTTP, API, MCP, console, and WebSocket route files, with application lifecycle hooks and a service provider ready for your own code. The framework implementation is installed as the `orionis` dependency.

## Requirements and setup

Use **Python 3.14+**, [uv](https://docs.astral.sh/uv/), and **Orionis 1.9.0 or later within 1.x**. `pyproject.toml` declares the supported framework range. The initial `uv sync` resolves dependencies and creates a local `uv.lock`.

Run commands from this application's root. For a new checkout, copy `.env.example` to `.env` if `.env` does not already exist. Use `cp .env.example .env` on POSIX shells or `Copy-Item .env.example .env` in PowerShell. Keep an existing application's environment values and key.

```shell
uv sync
uv run orionis key:generate
```

Orionis writes a missing `APP_KEY` to `.env` during startup. If `key:generate` reports that the key is already set, keep it. The example sets `APP_URL` to `http://127.0.0.1:8000`, matching the development server. Adjust it to the application's base URL and review the selected services in `config/`. `.env.reference` documents additional configuration variables.

## Run and test

```shell
uv run orionis serve
uv run orionis test
uv run ruff check .
```

`serve` starts the development server; stop it before running other foreground commands in the same terminal. Inspect registered routes with `uv run orionis route:list` and available commands with `uv run orionis list`. The bundled `reactor` script remains an alternative, for example `uv run python -B reactor test`.

## Start building

The framework provides `GET /up` for health checks, plus its built-in favicon, robots, and sitemap routes. No application routes are predefined: a request to `/` returns `404` until you add one. For example, add this to `routes/web.py`:

```python
from orionis.http import PlainTextResponse
from orionis.support.facades import Route

def welcome() -> PlainTextResponse:
    """Greet the visitor."""
    return PlainTextResponse("Hello, Orionis")

Route.get("/", welcome)
```

Use `app/providers/app_service_provider.py` for application bindings, `bootstrap/lifespan.py` for lifecycle callbacks, and `app/exceptions/handler.py` for exception handling. The `config/` directory exposes the framework's service configuration even when your application does not use every service.

The empty extension directories follow the framework's canonical application paths and are tracked with `.gitkeep` so they survive cloning:

| Directory | Intended contents |
| --- | --- |
| `app/console/commands`, `app/console/listeners` | Commands and scheduler listeners. |
| `app/http/controllers`, `app/http/middleware`, `app/http/schemas/rules` | HTTP actions, middleware, schemas, and validation rules. |
| `app/mcp/servers`, `app/mcp/tools`, `app/mcp/resources`, `app/mcp/prompts` | MCP servers and their sibling capability directories. |
| `app/realtime/sockets`, `app/realtime/hubs` | Raw WebSocket handlers and realtime hubs. |
| `app/models`, `app/jobs`, `app/notifications` | Application models, queued jobs, and notification code. |
| `app/contracts`, `app/services`, `app/facades` | Service contracts, implementations, and facades. |
| `database/factories`, `database/migrations`, `database/schemas`, `database/seeders` | Application-owned data definitions and setup. |
| `resources/css`, `resources/js`, `resources/lang`, `resources/views` | Frontend source entry points, translations, and templates. |

The CSS and JavaScript entry files are empty, as in the framework's application structure. No frontend build tool is required or bundled. Publish browser assets to `storage/app/public` through your chosen build process; `resources/` is not a public static mount.

Add business models and migrations when your application needs them. `auth:migrate` creates the framework tables for roles, permissions, their three associations, personal access tokens, and password-reset tokens. The application owns its user table and privilege seeds. Each SQL-backed service has its own [internal storage command](https://docs.orionis-framework.com/en/database/commands#internal-storage-commands).

The template includes the `database/` directory for the default SQLite connection and `resources/views/` for your templates. SQLite creates `database/database.sqlite` when a SQL operation opens the connection. An alternative database path needs an existing parent directory as well.

Authentication is an extension point: add your identity model and its migrations before protecting routes. The default `AUTH_MODEL` expects `app.models.user.User`; no user model or authentication screens are included in this blank template.

The minimal environment uses SQLite, file cache and sessions, synchronous queues, and local application settings. It needs no external service to start. Configure mail if you add email-dependent features. Optional values and framework fallbacks remain in `.env.reference` and `config/`.

## Runtime compatibility

`app/exceptions/handler.py` uses `handleFailure(exception, context)` and `handleResult(value, context)`, returning the inherited deferred handling plan so the runtime can log and present failures once. Customize these hooks for application policy.

`config/app.py` defaults to authenticated `AES-256-GCM`, matching the framework. Before upgrading an existing application that uses CBC, migrate its encrypted values offline using the previous compatible framework version, then switch `APP_CIPHER` to a supported GCM cipher. Preserve the existing application key during the migration.

## Framework conventions

Class methods use `camelCase`, `_camelCase`, or `__camelCase`; functions outside classes use `snake_case`. Python protocol methods retain their required names, such as `__init__`. Document Python APIs with NumPy-style docstrings.

Schema validation remains strict outside the scope of an explicit `Coerce()` marker. Coercion runs before type, constraint, and rule checks; `Empty()` and `NoEmpty()` provide complementary empty-value rules. See [schema declarations](https://docs.orionis-framework.com/en/validation/declaring-schemas#field-coercion) and [empty-value rules](https://docs.orionis-framework.com/en/validation/application-rules#empty-and-no-empty) when defining application inputs. Query builders also support [`toSql()`](https://docs.orionis-framework.com/en/database/query-builder#api-tosql) for SQL inspection without executing a query.

## Project links

- [Framework source](https://github.com/orionis-framework/framework)
- [Skeleton variants](https://github.com/orionis-framework/skeleton)
- [Documentation](https://docs.orionis-framework.com/)
- [CLI installer](https://github.com/orionis-framework/installer)
- [Discussions](https://github.com/orgs/orionis-framework/discussions)
- [Support development](https://github.com/sponsors/rmunate)

Created and maintained by [Raul Mauricio Uñate Castro](https://github.com/rmunate). Released under the [MIT license](LICENCE).
