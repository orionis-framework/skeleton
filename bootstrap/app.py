from pathlib import Path
from orionis import Application
from app.console.scheduler import Scheduler
from app.exceptions.handler import ExceptionHandler
from app.providers.app_service_provider import AppServiceProvider
from bootstrap.lifespan import register_lifespan_callbacks

app = Application(base_path=Path(__file__).parent.parent)

app.compile(
    path="storage/framework/bootstrap",
    invalidation_paths=["app", "bootstrap", "config", "database", "routes", ".env"],
)

register_lifespan_callbacks(app)
app.withRouting(console="routes/console.py")
app.withScheduler(Scheduler)
app.withExceptionHandler(ExceptionHandler)
app.withProviders(AppServiceProvider)
app.create()
