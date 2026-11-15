__all__ = [
    "LibraryUseException",
    "MismatchedPlatforms",
    "MissingPermissions",
    "OperationException",
    "ResourceNotFound",
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
