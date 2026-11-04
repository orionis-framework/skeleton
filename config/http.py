from dataclasses import dataclass, field
from orionis.environment import Env
from orionis.foundation.config.http import (
    HTTP, HTTPProxies, HTTPSecurity, HTTPWebSocket,
)

@dataclass(frozen=True, kw_only=True)
class BootstrapHTTP(HTTP):
    """Configure WebSocket admission and the HTTP health endpoint."""

    websocket: HTTPWebSocket | dict = field(
        default_factory=lambda: HTTPWebSocket(
            max_connections=Env.get("WEBSOCKET_MAX_CONNECTIONS", 128),
            max_message_size=Env.get("WEBSOCKET_MAX_MESSAGE_SIZE", 1024 * 1024),
            allow_origins=Env.get("CORS_ALLOW_ORIGINS", ()),
        ),
    )

    proxies: HTTPProxies | dict = field(
        default_factory=lambda: HTTPProxies(
            trusted_proxies=Env.get("TRUSTED_PROXIES", ["127.0.0.1"]),
        ),
    )

    security: HTTPSecurity | dict = field(
        default_factory=lambda: HTTPSecurity(
            allowed_hosts=Env.get("ALLOWED_HOSTS", []),
        ),
    )
