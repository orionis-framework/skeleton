from orionis.http import JSONResponse, response
from orionis.http.base import BaseController

class HomeController(BaseController):

   async def health(self) -> JSONResponse:
        """
        Return the health status of the API.

        Returns
        -------
        JSONResponse
            A JSON response indicating the health status of the API.
        """
        return response.json({
            "message": "Orionis API is working",
            "status": "healthy",
        })
