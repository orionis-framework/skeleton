from typing import ClassVar
from orionis.auth.middleware import RequirePermissionMiddleware


class AdministrationMiddleware(RequirePermissionMiddleware):
    """Require the application's administration permission."""

    __slots__ = ()

    permissions: ClassVar[tuple[str, ...]] = ("full_access",)
