__all__ = [
    "BadRequest",
    "Forbidden",
    "GenericGatewayException",
    "GenericHTTPException",
    "GenericNotFound",
    "LibraryUseException",
    "MismatchedPlatforms",
    "MissingPermissions",
    "OperationException",
    "RateLimited",
    "ResourceNotFound",
    "Unauthorized",
    "UninitializableResource",
]

from abc import ABC
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .models.permissions import Permissions
    from .platform import Platform


class LibraryUseException(ABC, BaseException):
    """
    A class of exceptions that is raised when someone violates the way that this library is designed.
    """


class UninitializableResource(LibraryUseException):
    """
    This exception is raised when a resource that cannot be initialized is initialized.
    """

    def __init__(self, resource_type: str) -> None:
        super().__init__(f"{resource_type} cannot be initialized from user code.")


class MismatchedPlatforms(LibraryUseException):
    """
    This exception is raised when two values that are bound to platforms do not have the same platform.
    """

    def __init__(self, *values: Platform) -> None:
        super().__init__(
            f"Requires platforms to be the same, instead got {', '.join(repr(v) for v in values)}."
        )


class OperationException(ABC, RuntimeError):
    """
    A class of exceptions that is raised during the operation process of the client.
    """


class GenericHTTPException(OperationException):
    """
    This exception is raised when an HTTP request fails, and the library does not know what it means.
    """

    def __init__(self, status: int, message: str) -> None:
        super().__init__(f"Error {status}: {message}")


class GenericGatewayException(OperationException):
    """
    This exception is raised when the gateway experiences errors.
    """


class MissingPermissions(OperationException):
    """
    This exception is raised when the client does not have the permissions required to perform a certain action.
    """

    def __init__(self, missing: Permissions) -> None:
        super().__init__(
            f"The client does not have the permissions required to perform the action. Missing permissions: {', '.join(str(p) for p in missing)}."
        )


class ResourceNotFound(OperationException):
    """
    This exception is raised when the client cannot find a specific resource in a get operation.
    """

    def __init__(self, resource_type: str, ident: str) -> None:
        super().__init__(
            f"The corresponding {resource_type} ({ident}) could not be found."
        )


class BadRequest(OperationException):
    """
    This exception is raised when a request is malformed.
    """


class Unauthorized(OperationException):
    """
    This exception is raised when the client is unauthorized to perform a certain action.
    """


class Forbidden(OperationException):
    """
    This exception is raised when the client is forbidden to perform a certain action.
    """


class GenericNotFound(OperationException):
    """
    This exception is raised when the client cannot find a specific resource in a get operation.

    This exception is raised before it gets processed by methods into :class:`ResourceNotFound`.
    """


class RateLimited(OperationException):
    """
    This exception is raised when the client is ratelimited.
    """
