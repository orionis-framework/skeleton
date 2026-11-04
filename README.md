<p align="center">
  <img src="https://orionis-framework.com/favicon.svg" alt="Orionis Framework" width="180" />
</p>

<h1 align="center">Orionis Slim API Skeleton</h1>

<p align="center">Write Python. Build the whole application.</p>

<p align="center">
  <a href="https://docs.orionis-framework.com/">Documentation</a> &bull;
  <a href="https://api.orionis-framework.com/">API reference</a> &bull;
  <a href="https://orionis-framework.com/">Website</a>
</p>

This is the **minimal HTTP API skeleton** from the `slim_api_1.x` branch. It registers API routes and a health endpoint, with a global middleware, a service provider, and an exception handler. The framework implementation is installed as the `orionis` dependency.

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

## Included routes and extension points

- `GET /api/example`: `HomeController.health()` returns the example API status as JSON.
- `GET /up`: the built-in application health endpoint.
- `routes/api.py`: add API routes here; the example is grouped under `/api`.
- `app/http/middleware/global_middleware.py`: the initial middleware delegates to the next handler.
- `app/providers/app_service_provider.py`: register application services.

There is no browser welcome route at `/`, and WEB, WebSocket, console-route, and MCP files are not registered by this variant. Native CLI commands, including `test` and `serve`, remain available. Add another runtime explicitly in `bootstrap/app.py` when your application needs it.

The example endpoint is public. `config/auth.py` selects the token guard for optional API authentication. Before protecting routes, create an identity model and its business migrations, set `AUTH_MODEL` if its path differs from `app.models.user.User`, and prepare token storage with `uv run orionis auth:migrate`. This minimal template does not include a user model or browser login flow.

## Configuration and application data

The API configuration includes `app`, `http`, `auth`, `hashing`, `database`, `cache`, `filesystems`, `logging`, `mail`, `queue`, and `testing`. `http.py` exposes request and upload limits, trusted proxies, allowed hosts, CORS, and rate limiting. Browser sessions, views, MCP, Realtime, and scheduler configuration are not part of this variant. Add their configuration and runtime registration explicitly if your application needs those services.

The template has no application migrations. The example endpoint requires no tables. `database/migrations/`, `database/schemas/`, `database/factories/`, and `database/seeders/` contain only placeholders for application-owned data; add models under `app/models/` and request schemas under `app/http/schemas/`. If you enable SQL token, cache, or queue storage, use the relevant [internal storage command](https://docs.orionis-framework.com/en/database/commands#internal-storage-commands) with its configured connection. Business tables still require application migrations.

The tracked `database/` directory is ready for the default SQLite connection. SQLite creates `database/database.sqlite` when a SQL operation first opens it; database files and their journal sidecars are excluded from Git. An alternative database path needs an existing parent directory.

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
