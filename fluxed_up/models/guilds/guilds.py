__all__ = ["Guild", "GuildID"]

from typing import TYPE_CHECKING, Protocol

from ..model import Model
from ..snowflake import Snowflake

if TYPE_CHECKING:
    from ...exceptions import MissingPermissions, ResourceNotFound  # noqa # used in docstring
    from ..channels.channels import Channel, ChannelID
    from ..users import UserID
    from .roles import Role
    from .members import Member


class GuildID(Snowflake):
    """
    A :class:`Snowflake` representing a guild ID.
    """


class Guild(Model, Protocol):
    """
    Represents a guild, community, server, etc., on a platform.

    .. traits::
        .. trait:: eq
            .. based-on:: ID
        .. trait:: repr
            .. based-on:: ID

    Attributes
    ----------
    id : :class:`GuildID`
        The ID of this Guild.
    name : str
        The name of this Guild.
    owner_id : :class:`UserID`
        The owner of this Guild.
    roles : list[:class:`Role`]
        The roles of this Guild.
    channels : list[:class:`Channel`]
        The channels of this Guild.
    """

    id: GuildID
    name: str
    owner_id: UserID
    roles: list[Role]
    channels: list[Channel]

    async def get_channel(self, channel_id: ChannelID) -> Channel:
        """
        Gets a :class:`Channel` from this Guild.

        |coro|

        Parameters
        ----------
        channel_id : :class:`ChannelID`
            The ID of the channel to get.

        Returns
        -------
        :class:`Channel`
            The obtained channel.

        Raises
        ------
        :exc:`ResourceNotFound`
            The client could not find the specified channel in this Guild.

        See Also
        --------
        :meth:`Client.get_channel`
        """
        raise NotImplementedError

    async def me(self) -> Member:
        """
        Gets your own guild :class:`Member`.

        |coro|

        Returns
        -------
        :class:`Member`
            Your own guild Member.
        """
        raise NotImplementedError

    async def get_member(self, user_id: UserID) -> Member:
        """
        Gets a :class:`Member` from this Guild.

        |coro|

        Parameters
        ----------
        user_id : :class:`UserID`
            The ID of the user to get.

        Returns
        -------
        :class:`Member`
            The obtained member.

        Raises
        ------
        :exc:`ResourceNotFound`
            The client could not find the specified member.
        """
        raise NotImplementedError
