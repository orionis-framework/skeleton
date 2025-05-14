from flaskavel.lab.alchemist.http.base_controller import BaseController
from flaskavel.lab.reagents.response import Response
from flaskavel.lab.app import Application

class ExampleController(BaseController):
    """
    Handles HTTP requests for the example controller.
    """

    def index(self):
        """
        Handles the request for the 'index' endpoint. Responds with basic
        information about the framework, such as its name and version.

        Returns:
            Response: A JSON response with details about the framework.
        """
        framework_info = {
            'framework': Application.name.upper(),
            'version': Application.version,
        }

        return Response.success(
            data=framework_info,
            message="Welcome Aboard"
        )
