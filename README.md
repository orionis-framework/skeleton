<p align="center">
  <img src="https://orionis-framework.com/favicon.svg" alt="Orionis Framework" width="180" />
</p>

<h1 align="center">Orionis Slim Worker Skeleton</h1>

<p align="center">Run commands, consume queued jobs, and schedule background work.</p>

<p align="center">
  <a href="https://docs.orionis-framework.com/">Documentation</a> &bull;
  <a href="https://api.orionis-framework.com/">API reference</a> &bull;
  <a href="https://orionis-framework.com/">Website</a>
</p>

This is the **CLI and background worker skeleton** from the `slim_worker_1.x` branch. It includes an importable queue job, a command that dispatches it, and a scheduler that runs the command once per minute. It registers application console routes only, without application HTTP routes, browser sessions, views, authentication scaffolding, MCP servers, or public assets. It runs as CLI processes and needs no web listener. The framework's built-in HTTP routes, including `/up`, can still appear if you run `route:list`.

## Requirements and setup

Use **Python 3.14+**, [uv](https://docs.astral.sh/uv/), and **Orionis 1.4 or later within 1.x**. Run commands from the application's root. Copy `.env.example` to `.env` for a new checkout: use `cp .env.example .env` on POSIX shells or `Copy-Item .env.example .env` in PowerShell. Preserve an existing application's environment and key.

```shell
uv sync
uv run orionis key:generate
uv run orionis queue:migrate
```

The initial `uv sync` creates a local `uv.lock`; that generated file is not included in the template. `key:generate` stores `APP_KEY` and preserves an existing key unless explicitly forced.

The example uses SQLite at `database/database.sqlite`, file cache, and the **database queue connection**. The tracked `database/.gitkeep` preserves the database directory in a fresh checkout. `queue:migrate` creates the framework's job and failed-job tables, preserving existing records. Configure another SQL connection before running it if needed. `.env.reference` documents optional application, database, filesystem, cache, logging, queue, scheduler, and testing settings.

## Dispatch and consume a job

```shell
uv run orionis app:dispatch-example --message "Hello from the queue"
uv run orionis queue:work --stop-when-empty
```

The command awaits queue submission and prints the job identifier. The producer exits after persisting the payload; the separate worker restores `app.jobs.log_message_job.LogMessageJob` and writes `Worker message: Hello from the queue` to `storage/logs/stack.log`. `--stop-when-empty` exits once no job is ready. Use `uv run orionis queue:work` for a continuously running consumer.

The example job stores only its message. Its logger is injected at execution time, so no service instance is serialized. Keep importable job classes under `app/jobs`; retain their module and class names while old messages remain queued. New jobs can be generated with `uv run orionis make:job YourJob`.

The job allows three attempts, a 30-second timeout, and retry delays of one and five seconds. Its timeout is below the database reservation period of 90 seconds. Real jobs should tolerate retries and avoid repeating non-idempotent effects. Inspect failed jobs with `uv run orionis queue:failed`.

## Schedule the producer

```shell
uv run orionis schedule:list
uv run orionis schedule:work
```

The example schedule enqueues one message every minute while `schedule:work` is running. Run a queue worker in a separate terminal or supervised process to consume those messages. Stop foreground processes before running unrelated commands in the same terminal. Customize or remove this example task before using the template for application workloads.

Scheduler definitions use the process-local `memory` store by default; queued messages remain in SQLite across process restarts. If you select `TASKS_STORE="database"`, prepare its table with `uv run orionis schedule:migrate`. If you select SQL-backed cache, prepare it with `uv run orionis cache:migrate`. The template does not duplicate these framework tables in application migrations.

## Application structure

- `bootstrap/app.py`: console routing, scheduler, providers, exception handler, and application creation.
- `bootstrap/lifespan.py`: generic and CLI startup/shutdown callbacks.
- `app/console/commands/dispatch_example_command.py`: the queue producer command.
- `app/console/scheduler.py`: the once-per-minute producer schedule.
- `app/jobs/log_message_job.py`: importable job and its serialized message.
- `app/providers/app_service_provider.py`: application service bindings.
- `routes/console.py`: extension point for additional console routes; command classes are discovered under `app/console/commands`.
- `config/`: application, database, cache, filesystems, logging, queues, scheduler, and testing configuration.
- `database/`: directory for the default SQLite database and future application migrations.
- `tests/`: serialization, execution, and awaited-dispatch regression tests without application database writes.

Runtime storage is created as needed. Environment files, databases, logs, cache files, and other private runtime output are excluded from version control.

The empty `storage/app/public/` directory is tracked because the framework's optional `serve` command requires that directory. Worker and scheduler processes do not need a web server.

## Test and extend

```shell
uv run orionis test
uv run ruff check .
uv run orionis list
```

The bundled `reactor` remains an alternative, for example `uv run python -B reactor test`. Class methods use `camelCase`, `_camelCase`, or `__camelCase`; functions outside classes use `snake_case`. Python protocol methods retain their required names. Document Python APIs with NumPy-style docstrings.

See the [framework documentation](https://docs.orionis-framework.com/) and [API reference](https://api.orionis-framework.com/) for queue, scheduler, database, and console APIs. The broader [application skeletons](https://github.com/orionis-framework/skeleton) provide web, API, MCP, and other runtime entry points.

Created and maintained by [Raul Mauricio Uñate Castro](https://github.com/rmunate). Released under the [MIT license](LICENCE).
