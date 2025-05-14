from flaskavel.lab.reagents.request import Request
from flaskavel.lab.reagents.response import Response
from flaskavel.lab.alchemist.http.base_middleware import BaseMiddleware

class ExampleMiddleware(BaseMiddleware):
    """
    Middleware that processes incoming HTTP requests before passing them
    to the next layer in the request handling pipeline.
    """

    def handle(self, next):
        """
        Intercepts the request and allows for custom logic before passing
        the request to the next middleware or controller.

        Args:
            next (Callable): The next middleware or handler in the pipeline.

        Returns:
            Response: The response from the next handler or middleware.
        """
        # Add custom logic here if needed, such as logging or modifying the request.

        return next()
