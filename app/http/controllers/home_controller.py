from orionis.http import HTMLResponse, response
from orionis.http.base import BaseController

class HomeController(BaseController):

    async def home(self) -> HTMLResponse:
        """
        Render the authenticated home page response.

        Returns
        -------
        HTMLResponse
            The rendered home page for the signed-in user.
        """
        return await response.view("home.index")
