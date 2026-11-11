__all__ = ["Snowflake"]

from abc import ABC
from functools import total_ordering

from ..platform import Platform


@total_ordering
class Snowflake(ABC):
    """
    Unique identifier of a specific model or resource.

    |ABC|

    This class can also be hashed, compared, and used as dictionary keys.
    Two Snowflakes are equal if they are the same type, have the same raw integer ID value, and are on the same platform.

    .. traits::
        .. trait:: eq
            .. type:: total
            .. based-on:: concrete type, raw integer ID, platform
        .. trait:: hash
            .. based-on:: concrete type, raw integer ID, platform
        .. trait:: ord
            .. type:: partial
            .. based-on:: raw ID
            Errors on mismatched type or platform.
        .. trait:: repr
            .. type:: construction
        .. trait:: str
            .. based-on:: raw ID

    Attributes
    ----------
    id : int
        The raw integer value of this Snowflake.
    platform : :class:`Platform`
        The platform that this Snowflake belongs to.

    Parameters
    ----------
    id : int | str
        The raw integer value of this Snowflake.
    platform : :class:`Platform`
        The platform that this Snowflake belongs to.
    """

    __slots__ = ("id", "platform")

    id: int
    platform: Platform

    def __init__(self, id: int | str, platform: Platform) -> None:
        """
        Creates a new Snowflake.

        Raises
        ------
        TypeError
            When initializing the Snowflake `ABC <https://docs.python.org/3/glossary.html#term-abstract-base-class>`_ directly.
        """
        if self.__class__ is Snowflake:
            raise TypeError(
                "Snowflake is an abstract class and should not be initiated directly. Instead, use one of its type-safe subtypes."
            )

        self.id = int(id)
        self.platform = platform

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.id}, {self.platform})"

    def __str__(self) -> str:
        return str(self.id)

    def __int__(self) -> int:
        return self.id

    def __hash__(self) -> int:
        return hash((type(self), self.id, self.platform))

    def __eq__(self, other: object) -> bool:
        return (
            type(self) is type(other)
            and isinstance(other, Snowflake)  # type hint for mypy
            and self.id == other.id
            and self.platform is other.platform
        )

    def __lt__(self, other: object) -> bool:
        if not isinstance(other, Snowflake):
            raise TypeError()

        if type(self) is not type(other):
            raise TypeError()

        if self.platform is not other.platform:
            raise TypeError()

        return self.id < other.id

    @property
    def timestamp(self) -> float:
        """
        Returns
        -------
        float
            The timestamp in seconds at which this Snowflake was issued.
        """
        return ((self.id >> 22) + self.platform.value.epoch_ms) / 1000
