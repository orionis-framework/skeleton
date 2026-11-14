from orionis.support.facades import Route
from app.http.controllers.home_controller import HomeController

Route.group(prefix="/api", routes=[
    Route.get("/example", [HomeController, "health"]),
])
