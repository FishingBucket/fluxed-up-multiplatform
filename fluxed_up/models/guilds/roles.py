__all__ = ["Role", "RoleID"]

from typing import Protocol

from ..model import Model
from ..snowflake import Snowflake


class RoleID(Snowflake):
    """
    A :class:`Snowflake` representing a role ID.
    """


class Role(Model, Protocol):
    """
    Represents a role for a platform.
    """

    id: RoleID
