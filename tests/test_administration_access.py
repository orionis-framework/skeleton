# ruff: noqa: PT027 -- Orionis TestCase uses unittest exception assertions.

from unittest.mock import AsyncMock, Mock, patch
from app.http.middleware.administration_middleware import AdministrationMiddleware
from orionis.auth.contracts.authorizer import IAuthorizer
from orionis.auth.contracts.context import IAuthenticationContext
from orionis.auth.exceptions import AuthenticationException, AuthorizationException
from orionis.http import Request, response
from orionis.test import TestCase


class TestAdministrationAccess(TestCase):

    async def testGuestCannotEnterAdministration(self) -> None:
        """
        Reject guests before checking permissions or invoking the controller.

        Returns
        -------
        None
            Verify that an anonymous context cannot advance the request.
        """
        context = Mock(spec=IAuthenticationContext, isGuest=True)
        authorizer = AsyncMock(spec=IAuthorizer)
        next_handler = AsyncMock()
        middleware = AdministrationMiddleware(authorizer)

        with (
            patch(
                "orionis.auth.middleware.authorize.current_auth_context",
                return_value=context,
            ),
            self.assertRaises(AuthenticationException),
        ):
            await middleware.handle(Mock(spec=Request), next_handler)

        authorizer.canAll.assert_not_awaited()
        next_handler.assert_not_awaited()

    async def testAccountWithoutFullAccessIsRejected(self) -> None:
        """
        Reject an authenticated account without administration permission.

        Returns
        -------
        None
            Verify that authentication alone does not authorize administration.
        """
        context = Mock(spec=IAuthenticationContext, isGuest=False)
        authorizer = AsyncMock(spec=IAuthorizer)
        authorizer.canAll.return_value = False
        next_handler = AsyncMock()
        middleware = AdministrationMiddleware(authorizer)

        with (
            patch(
                "orionis.auth.middleware.authorize.current_auth_context",
                return_value=context,
            ),
            self.assertRaises(AuthorizationException),
        ):
            await middleware.handle(Mock(spec=Request), next_handler)

        authorizer.canAll.assert_awaited_once_with(context, ("full_access",))
        next_handler.assert_not_awaited()

    async def testAccountWithFullAccessCanContinue(self) -> None:
        """
        Allow an account with the permission granted by the admin seeder.

        Returns
        -------
        None
            Verify that an authorized request returns the controller response.
        """
        context = Mock(spec=IAuthenticationContext, isGuest=False)
        authorizer = AsyncMock(spec=IAuthorizer)
        authorizer.canAll.return_value = True
        expected = response.text("Allowed")
        next_handler = AsyncMock(return_value=expected)
        middleware = AdministrationMiddleware(authorizer)

        with patch(
            "orionis.auth.middleware.authorize.current_auth_context",
            return_value=context,
        ):
            actual = await middleware.handle(Mock(spec=Request), next_handler)

        self.assertIs(actual, expected)
        authorizer.canAll.assert_awaited_once_with(context, ("full_access",))
        next_handler.assert_awaited_once_with()
