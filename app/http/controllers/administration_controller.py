from orionis.auth.contracts.manager import IAuthManager
from orionis.http import HTMLResponse, response
from orionis.http.base import BaseController

class AdministrationController(BaseController):

    async def roles(self, auth: IAuthManager) -> HTMLResponse:
        """
        Render the roles placeholder inside the authenticated layout.

        Parameters
        ----------
        auth : IAuthManager
            Authentication manager for the current user.

        Returns
        -------
        HTMLResponse
            Rendered roles page.
        """
        identity = auth.user()
        return await response.view(
            "admin.roles.index",
            user={"name": identity.name, "email": identity.email},
        )

    async def users(self, auth: IAuthManager) -> HTMLResponse:
        """
        Render the users placeholder inside the authenticated layout.

        Parameters
        ----------
        auth : IAuthManager
            Authentication manager for the current user.

        Returns
        -------
        HTMLResponse
            Rendered users page.
        """
        identity = auth.user()
        return await response.view(
            "admin.users.index",
            user={"name": identity.name, "email": identity.email},
        )
