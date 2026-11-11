__all__ = ["UninitializableResource", "UnmatchedPlatforms"]

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .platform import Platform


class UninitializableResource(Exception):
    """
    This exception is raised when a resource that cannot be initialized is initialized.
    """

    def __init__(self, resource_type: str) -> None:
        super().__init__(f"{resource_type} cannot be initialized from user code.")


class UnmatchedPlatforms(Exception):
    """
    This exception is raised when two values that are bound to platforms do not have the same platform.
    """

    def __init__(self, *values: Platform) -> None:
        super().__init__(
            f"Requires platforms to be the same, instead got {', '.join(repr(v) for v in values)}."
        )
