__all__ = ["Platform", "PlatformData"]

import itertools
from dataclasses import dataclass
from enum import Enum

from .exceptions import MismatchedPlatforms


@dataclass
class PlatformData:
    """
    Data about a supported platform.
    """

    name: str
    epoch_ms: int

    def __repr__(self) -> str:
        return self.name

    def __str__(self) -> str:
        return self.name


class Platform(Enum):
    """
    An enum representing all supported platforms of this library.

    .. traits::
        .. trait:: eq
            Enum equality, unless one of the operands is :enum:mem:`Platform.Auto`.
        .. trait:: hash
        .. trait:: repr
            .. type:: construction
        .. trait:: str
            The name of the current platform.

    Notes
    -----
    The :enum:mem:`Platform.Auto` enum member represents a situation where the platform of a resource cannot be determined or is not provided.
    """

    Auto = PlatformData("Auto", 0)  # automatically determined
    Fluxer = PlatformData("Fluxer", 1420070400000)
    Discord = PlatformData("Discord", 1420070400000)

    def __repr__(self) -> str:
        return "Platform." + self.name

    def __str__(self) -> str:
        return str(self.name)

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Platform) and (
            self is other or self is Platform.Auto or other is Platform.Auto
        )

    def __hash__(self) -> int:
        return hash("Platform." + self.name)

    @staticmethod
    def raise_if_unmatched(*platforms: Platform | None) -> None:
        """
        Checks for all inputs and raise an exception if one of the inputs is unmatched.

        Parameters
        ----------
        platforms : Sequence[Platform]
            The platforms to check.

        Raises
        ------
        :exc:`MismatchedPlatforms`
            If even one of the platforms is unmatched.
        """
        without_none = tuple(platform for platform in platforms if platform)
        for a, b in itertools.pairwise(without_none):
            if a != b:
                raise MismatchedPlatforms(*without_none)
