from flaskavel.lab.beaker.routes.router import Route

Route.middleware(['csrf']).prefix('v1').controller('ExampleController').group(
    Route.get("/", "index").name("example.index"),
)