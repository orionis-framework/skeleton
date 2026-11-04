<p align="center">
  <img src="https://orionis-framework.com/favicon.svg" alt="Orionis Framework" width="180" />
</p>

<h1 align="center">Orionis Application Skeleton</h1>

<p align="center">Write Python. Build the whole application.</p>

<p align="center">
  <a href="https://docs.orionis-framework.com/">Documentation</a> &bull;
  <a href="https://api.orionis-framework.com/">API reference</a> &bull;
  <a href="https://orionis-framework.com/">Website</a>
</p>

This is the full **application skeleton** from the repository's `master` branch. It provides server-rendered authentication and administration pages, an API example, and route extension points for console commands, WebSockets, and MCP. The framework implementation is installed as the `orionis` dependency.

The application layout follows the framework repository's `app/`, `bootstrap/`, `config/`, `database/`, `resources/`, `routes/`, and public assets. All 17 application configuration modules are included. Framework library sources, its internal test suite, and API documentation build tools remain in the framework repository rather than the generated application.

## Choose a skeleton

Each variant is distributed as a branch of this repository:

| Branch | Starting point |
| --- | --- |
| [`master`](https://github.com/orionis-framework/skeleton/tree/master) | Full application with web authentication, permission-protected administration, an API example, and additional runtime extension points. |
| [`ssr_1.x`](https://github.com/orionis-framework/skeleton/tree/ssr_1.x) | Server-rendered web application with authentication and administration. |
| [`blank_1.x`](https://github.com/orionis-framework/skeleton/tree/blank_1.x) | Empty application with route extension points for every runtime and the complete configuration surface. |
| [`slim_api_1.x`](https://github.com/orionis-framework/skeleton/tree/slim_api_1.x) | JSON API with a public example endpoint and optional token authentication configuration. |
| [`slim_mcp_1.x`](https://github.com/orionis-framework/skeleton/tree/slim_mcp_1.x) | MCP server with typed tool, resource, and prompt examples plus protocol tests. |
| [`slim_worker_1.x`](https://github.com/orionis-framework/skeleton/tree/slim_worker_1.x) | Console application with a durable SQL queue, an example job, and scheduled dispatch. |
| [`slim_realtime_1.x`](https://github.com/orionis-framework/skeleton/tree/slim_realtime_1.x) | Dedicated WebSocket and hub RPC service with echo examples. |

## Requirements and setup

Use **Python 3.14+**, [uv](https://docs.astral.sh/uv/), and **Orionis 1.5 or later within 1.x**. `pyproject.toml` declares the supported framework range. The initial `uv sync` resolves dependencies and creates a local `uv.lock`; that generated file is not included in this template.

Run commands from this application's root. For a new checkout, copy `.env.example` to `.env` if `.env` does not already exist. Use `cp .env.example .env` on POSIX shells or `Copy-Item .env.example .env` in PowerShell. Keep an existing application's environment values and key.

```shell
uv sync
uv run orionis key:generate
```

`key:generate` stores a new `APP_KEY` in `.env` and preserves an existing key unless explicitly forced. The example sets `APP_URL` to `http://127.0.0.1:8000`, matching the development server. Adjust it to the application's base URL and review the selected services in `config/`. `.env.reference` documents additional configuration variables.

## Prepare application data

The default SQL connection is SQLite at `database/database.sqlite`. Configure a different connection in `.env` and `config/database.py` before preparing its tables. Create the application's `users` table, then prepare the framework's authentication and authorization tables:

```shell
uv run orionis migrate
uv run orionis auth:migrate
```

`auth:migrate` creates `permissions`, `roles`, `model_has_permissions`, `model_has_roles`, `role_has_permissions`, personal access tokens, and password-reset storage. Run it before logging in, using recovery links, or running the optional seeder. These framework tables do not add entries to application migration history.

With `.env.example`, sessions and cache use `file`, queues use `sync`, and the scheduler defaults to `memory`. Sessions persist in `storage/framework/sessions`. Mail uses the `file` transport with an example sender, saving messages in `storage/mail` for local inspection; configure SMTP and a real sender to deliver email. If you choose database sessions or another SQL-backed service, prepare that service with its command below before starting requests or workers.

An optional demonstration seeder creates the `admin` role, the `full_access` permission, and an account with a fixed example password. Review and customize `database/seeders/s0000000001_create_admin_authorization.py` before running `uv run orionis seed`; the bundled account is intended for local development, not production provisioning. Seeding is not required to run the welcome page or health endpoints.

## Run and test

```shell
uv run orionis serve
uv run orionis test
uv run ruff check .
```

`serve` starts the development server; stop it before running other foreground commands in the same terminal. Inspect registered routes with `uv run orionis route:list` and available commands with `uv run orionis list`. The bundled `reactor` script remains an alternative, for example `uv run python -B reactor test`.

## Application structure

- `bootstrap/app.py`: application construction, route registration, service providers, lifecycle callbacks, middleware, and scheduler.
- `routes/web.py`: welcome page, authentication, profile, and administration routes.
- `routes/api.py`: the example `GET /api/health` endpoint.
- `routes/ai.py`, `routes/console.py`, and `routes/websocket.py`: extension points for the other runtime contexts.
- `app/http/controllers/` and `app/http/schemas/`: application actions and validated inputs.
- `app/console/listeners/`, `app/http/schemas/rules/`, and `app/jobs/`: console listeners, validation rules, and queued jobs.
- `app/contracts/`, `app/facades/`, `app/notifications/`, and `app/services/`: extension points using the framework's standard directory names.
- `app/mcp/` and `app/realtime/`: standard server/tool/resource/prompt and socket/hub directories, ready for registrations in their route files.
- `resources/views/` and `resources/lang/`: server-rendered views and translations.
- `storage/app/public/`: public assets supplied with this template.
- `database/`: application migrations, versioned business schemas, factories, and seeders.
- `tests/`: application tests discovered by `orionis test`.

After setup, open `/` for the welcome page, `/api/health` for the example JSON response, or `/up` for the built-in health endpoint. Authentication pages require the application tables. The administration placeholders require the `full_access` permission, granted to the demo `admin` role by the optional seeder; ordinary accounts can use their dashboard and profile without it.

## Framework storage tables

Orionis 1.5 owns authorization, personal access token, and password-reset schemas. The project therefore keeps only `m0000000005_create_users_table.py` and `users_v1.py`, alongside the user factory and optional demonstration seeder. It does not duplicate framework storage schemas or migrations. `auth:migrate` is required for the included authentication and administration flows; prepare other services only when you select their SQL-backed drivers:

| Service | Preparation command | Configuration |
| --- | --- | --- |
| Authorization, access tokens, and password recovery | `uv run orionis auth:migrate` | Default SQL connection; `AUTH_TOKEN_TABLE` and `AUTH_PASSWORD_RESET_TABLE` select the configurable token tables. |
| SQL cache and locks | `uv run orionis cache:migrate` | `DB_CACHE_CONNECTION`, `DB_CACHE_TABLE`, `DB_CACHE_LOCK_TABLE`. |
| SQL queues and failed jobs | `uv run orionis queue:migrate` | Configured SQL queue connections and failure storage. |
| Persistent scheduler | `uv run orionis schedule:migrate` | `DB_TASK_CONNECTION`, `DB_TASK_TABLE`. |
| SQL sessions | `uv run orionis session:migrate` | `SESSION_DB_CONNECTION`, `SESSION_DB_TABLE`. |

These commands create missing tables from the framework definitions and preserve existing records. They do not execute application migrations, change incompatible schemas, or write migration history. They accept no `--database` option; select their connections in configuration. Scheduler storage uses its native table name directly; the other services honor the SQL connection prefix. See the [storage preparation guide](https://docs.orionis-framework.com/en/database/migrations#framework-storage-tables).

When updating an existing application, keep its applied migrations, their schemas, and migration history so rollback can still resolve them. The removed duplicate templates are not a request to delete existing project history or data. The user migration retains its original `m0000000005` number.

## Conventions and validation

Class methods use `camelCase`, `_camelCase`, or `__camelCase`; functions outside classes use `snake_case`. Python protocol methods retain their required names, such as `__init__`. Document Python APIs with NumPy-style docstrings.

Schema validation remains strict outside the scope of an explicit `Coerce()` marker. Coercion runs before type, constraint, and rule checks; `Empty()` and `NoEmpty()` are complementary empty-value rules. See [schema declarations](https://docs.orionis-framework.com/en/validation/declaring-schemas#field-coercion) and [empty-value rules](https://docs.orionis-framework.com/en/validation/application-rules#empty-and-no-empty) when defining application inputs. Query builders also support [`toSql()`](https://docs.orionis-framework.com/en/database/query-builder#api-tosql) for SQL inspection without executing a query.

## Project links

- [Framework source](https://github.com/orionis-framework/framework)
- [Skeleton variants](https://github.com/orionis-framework/skeleton)
- [Documentation](https://docs.orionis-framework.com/)
- [CLI installer](https://github.com/orionis-framework/installer)
- [Discussions](https://github.com/orgs/orionis-framework/discussions)
- [Support development](https://github.com/sponsors/rmunate)

Created and maintained by [Raul Mauricio Uñate Castro](https://github.com/rmunate). Released under the [MIT license](LICENCE).
