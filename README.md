<p align="center">
  <img src="https://orionis-framework.com/favicon.svg" alt="Orionis Framework" width="180" />
</p>

<h1 align="center">Orionis Slim Realtime Skeleton</h1>

<p align="center">Write Python. Build the whole application.</p>

<p align="center">
  <a href="https://docs.orionis-framework.com/">Documentation</a> &bull;
  <a href="https://api.orionis-framework.com/">API reference</a> &bull;
  <a href="https://orionis-framework.com/">Website</a>
</p>

This is the **dedicated WebSocket and realtime RPC skeleton** for the `slim_realtime_1.x` branch. It provides a raw text socket, a typed Hub method, and an HTTP health endpoint. Application configuration covers runtime settings, HTTP/WebSocket admission, Realtime limits, logging, and testing. It starts without application models, database configuration, sessions, authentication flows, or templates.

## Requirements and setup

Use **Python 3.14+**, [uv](https://docs.astral.sh/uv/), and **Orionis 1.4 or later within 1.x**. The framework implementation is installed as the `orionis` dependency. The initial `uv sync` resolves dependencies and creates a local `uv.lock`; that generated file is not included in this template.

Run commands from the application's root. Copy `.env.example` to `.env` if `.env` does not already exist: use `cp .env.example .env` on POSIX shells or `Copy-Item .env.example .env` in PowerShell. Keep an existing application's environment values and key.

```shell
uv sync
uv run orionis key:generate
```

`key:generate` preserves an existing key unless explicitly forced. `APP_URL` starts at `http://127.0.0.1:8000`, matching the development server. Advanced settings are listed in `.env.reference`.

## Run and test

```shell
uv run orionis serve
uv run orionis test
uv run ruff check .
```

`serve` starts the development server; stop it before running other foreground commands in the same terminal. Inspect routes with `uv run orionis route:list` and commands with `uv run orionis list`. The bundled `reactor` script remains an alternative, for example `uv run python -B reactor test`.

`tests/test_realtime.py` exercises the real ASGI application with queued client events. It verifies socket acceptance, text echo, Hub ready/completion messages, rejection of malformed RPC and unregistered methods, origin checks, and connection cleanup. These tests do not open network ports or require a database.

## Included endpoints

| Endpoint | Purpose |
| --- | --- |
| `GET /up` | Built-in HTTP health response. |
| `WS /ws/echo` | Raw socket accepting and returning text frames. |
| `WS /realtime/echo` | JSON Hub RPC exposing the typed `echo(message: str)` method. |

`routes/websocket.py` registers both WebSocket routes. `app/realtime/sockets/echo_socket.py` implements the raw socket; `app/realtime/hubs/echo_hub.py` implements the Hub. `bootstrap/lifespan.py` provides startup and shutdown hooks, and `app/providers/app_service_provider.py` is the service registration point. The example exception handler supports CLI and HTTP errors.

Only WebSocket routes and health are registered in `bootstrap/app.py`. Native CLI commands remain available. The root `/` is not a browser application page.

The tracked `storage/app/public/.gitkeep` preserves the public directory required by the development server, even though this template includes no frontend assets.

## Try the raw socket

Open `http://127.0.0.1:8000/up` and run the following in that page's browser console so the handshake uses the same origin:

```javascript
const socket = new WebSocket("ws://127.0.0.1:8000/ws/echo");
socket.onopen = () => socket.send("Hello Orionis");
socket.onmessage = (event) => {
  console.log(event.data); // Hello Orionis
  socket.close();
};
```

The raw endpoint accepts text frames and returns their contents unchanged. It does not interpret Hub envelopes.

## Try Hub RPC

Run this from the same page's console. Wait for the `ready` envelope before invoking a method:

```javascript
const hub = new WebSocket("ws://127.0.0.1:8000/realtime/echo");
hub.onmessage = (event) => {
  const message = JSON.parse(event.data);
  if (message.type === "ready") {
    console.log(message.version, message.connection_id);
    hub.send(JSON.stringify({
      type: "invoke",
      id: "echo-1",
      target: "echo",
      args: ["Hello Orionis"],
    }));
  } else if (message.type === "completion" && message.id === "echo-1") {
    if (message.error) console.error(message.error);
    else console.log(message.result); // Hello Orionis
    hub.close();
  }
};
```

The server returns `{"type":"completion","id":"echo-1","result":"Hello Orionis"}`. Only methods decorated with `@remote` are exposed. Malformed JSON closes a Hub connection with code `1002`; invocation errors are correlated to the call ID. See the [protocol guide](https://docs.orionis-framework.com/en/realtime/protocol-and-streaming) for the complete envelope format and the [JavaScript client](https://docs.orionis-framework.com/en/realtime/javascript-client) for higher-level clients.

## Origins, limits, and deployment

With `CORS_ALLOW_ORIGINS` unset, browser connections must have the same origin as the requested socket. For a separate frontend, add its exact origin in `.env`, for example `CORS_ALLOW_ORIGINS="list:['http://127.0.0.1:5173']"`. Use `wss://` when serving the frontend over HTTPS. Non-browser clients without an `Origin` header are accepted. Both examples are public; add handshake authentication and application authorization when exposing protected operations.

`config/http.py` controls concurrent connections, raw message size, trusted proxies, and allowed hosts. `config/realtime.py` controls Hub message size, concurrent calls, pending client results, timeouts, groups, and broadcast concurrency. Defaults bound connections to 128 per worker and messages to 1 MiB. Ordinary invocation timeouts do not terminate long-lived sockets or streams.

Connection tracking, groups, and broadcasts are local to each worker process. Starting multiple workers does not create a shared group registry or an automatic Redis backplane. Choose a deployment and an explicit cross-process distribution mechanism that match the application's delivery requirements; see [groups and deployment](https://docs.orionis-framework.com/en/realtime/groups-and-deployment).

## Conventions

Class methods use `camelCase`, `_camelCase`, or `__camelCase`; functions outside classes use `snake_case`. Python protocol methods retain their required names, such as `__call__`. Document Python APIs with NumPy-style docstrings.

## Project links

- [Framework source](https://github.com/orionis-framework/framework)
- [Skeleton variants](https://github.com/orionis-framework/skeleton)
- [Documentation](https://docs.orionis-framework.com/)
- [CLI installer](https://github.com/orionis-framework/installer)
- [Discussions](https://github.com/orgs/orionis-framework/discussions)
- [Support development](https://github.com/sponsors/rmunate)

Created and maintained by [Raul Mauricio Uñate Castro](https://github.com/rmunate). Released under the [MIT license](LICENCE).
