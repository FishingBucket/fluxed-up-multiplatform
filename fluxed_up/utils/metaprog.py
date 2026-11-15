__all__ = ["require_permissions"]

from collections.abc import Callable
from typing import TYPE_CHECKING, Protocol, cast

if TYPE_CHECKING:
    from ..models.permissions import Permissions


class APIFunc[**P, T](Protocol):
    permissions_fluxer: Permissions
    permissions_discord: Permissions
    __call__: Callable[P, T]


def require_permissions[**P, T](
    permissions: Permissions,
    *,
    permissions_fluxer: Permissions | None = None,
    permissions_discord: Permissions | None = None,
) -> Callable[[Callable[P, T]], APIFunc[P, T]]:
    """
    Annotates an API function with the permissions it requires.

    Parameters
    ----------
    permissions : :class:`Permissions`
        The permissions that the API function requires for all platforms.

    Other Parameters
    ----------------
    permissions_fluxer : :class:`Permissions` | None, default=None
        Fluxer-specific permissions. Optional.
    permissions_discord : :class:`Permissions` | None, default=None
        Discord-specific permissions. Optional.

    Returns
    -------
    decorator
        A decorator to apply these annotations to the function.
    """
    permissions_fluxer = (
        (permissions | permissions_fluxer) if permissions_fluxer else permissions
    )
    permissions_discord = (
        (permissions | permissions_discord) if permissions_discord else permissions
    )

    def wrapper(func: Callable[P, T]) -> APIFunc[P, T]:
        new_func: APIFunc[P, T] = cast(APIFunc[P, T], func)
        new_func.permissions_fluxer = permissions_fluxer
        new_func.permissions_discord = permissions_discord
        return new_func

    return wrapper
