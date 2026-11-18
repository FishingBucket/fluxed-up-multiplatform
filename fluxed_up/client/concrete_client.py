__all__ = ["ConcreteClient"]

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..exceptions import ResourceNotFound  # noqa # used in docs
    from ..models.guilds.guilds import Guild, GuildID
    from ..models.users import User, UserProfile, UserID
    from ..models.channels.channels import ChannelID, Channel
    from ..models.messages.messages import MessageRef, Message


class ConcreteClient(ABC):
    """
    An abstract base class for concrete client implementations.

    |ABC|
    """

    user: User
    profile: UserProfile

    @property
    @abstractmethod
    def latency(self) -> float:
        """
        Returns
        -------
        float
            The live gateway latency in seconds.
        """
        raise NotImplementedError

    @abstractmethod
    async def get_http_latency(self) -> float:
        """
        Makes a mock request to the API to get the HTTP API latency.

        Returns
        -------
        float
            The latency in seconds.
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def guilds(self) -> list[Guild]:
        """
        Returns
        -------
        list[:class:`Guild`]
            The list of guilds that this client sees. This might not contain all guilds that the client is added in.
        """
        raise NotImplementedError

    @abstractmethod
    async def get_guild(self, guild_id: GuildID) -> Guild:
        """
        Get a :class:`Guild` by its ID.

        |coro|

        Parameters
        ----------
        guild_id : :class:`GuildID`
            The ID of the Guild to get.

        Returns
        -------
        :class:`Guild`
            The obtained Guild.

        Raises
        ------
        :exc:`ResourceNotFound`
            If the requested Guild does not exist.
        """
        raise NotImplementedError

    @abstractmethod
    async def get_channel(self, channel_id: ChannelID) -> Channel:
        """
        Get a :class:`Channel` by its ID.

        |coro|

        Parameters
        ----------
        channel_id : :class:`ChannelID`
            The ID of the Channel to get.

        Returns
        -------
        :class:`Channel`
            The obtained Channel.

        Raises
        ------
        :exc:`ResourceNotFound`
            If the requested Channel does not exist.
        """
        raise NotImplementedError

    @abstractmethod
    async def get_user(self, user_id: UserID) -> User:
        """
        Get a :class:`User` by its ID.

        |coro|

        Parameters
        ----------
        user_id : :class:`UserID`
            The ID of the User to get.

        Returns
        -------
        :class:`User`
            The obtained User.

        Raises
        ------
        :exc:`ResourceNotFound`
            If the requested User does not exist.
        """
        raise NotImplementedError

    @abstractmethod
    async def get_message(self, ref: MessageRef) -> Message:
        """
        Get a :class:`Message` by its ID.

        |coro|

        Parameters
        ----------
        ref : :class:`MessageRef`
            The ID of the Message to get.

        Returns
        -------
        :class:`Message`
            The obtained Message.

        Raises
        ------
        :exc:`ResourceNotFound`
            If the requested Message does not exist.
        """
        raise NotImplementedError
