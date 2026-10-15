from pathlib import Path
from orionis import Application
from app.exceptions.handler import ExceptionHandler
from app.http.middleware.global_middleware import GlobalMiddleware
from app.providers.app_service_provider import AppServiceProvider

# Create the application instance with caching enabled.
app = Application(
    base_path=Path(__file__).parent.parent,
)

# Compile the application with caching and invalidation paths.
app.compile(
    path="storage/framework/bootstrap",
    invalidation_paths=[
        "app",
        "bootstrap",
        "config",
        "database",
        "resources",
        "routes",
        ".env",
    ],
)

# Register route files for the different runtime contexts.
app.withRouting(
    api="routes/api.py",
    websocket="routes/websocket.py",
    health="/up",
)

# Set the global exception handler for unhandled exceptions.
app.withExceptionHandler(ExceptionHandler)

# Register service providers for dependency injection.
app.withProviders(
    AppServiceProvider,
    # ...
)

# Register global middleware for HTTP request processing.
app.withMiddleware(
    GlobalMiddleware,
    # ...
)

# Boot the application and prepare the runtime environment.
app.create()
