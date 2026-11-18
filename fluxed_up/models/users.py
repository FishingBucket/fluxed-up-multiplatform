from enum import IntFlag
from typing import TYPE_CHECKING, Protocol

from ..utils import Color
from .model import Model
from .snowflake import Snowflake

if TYPE_CHECKING:
    from ..exceptions import MissingPermissions  # noqa # used in docs
    from .channels.channels import Channel

__all__ = ["Discriminator", "User", "UserID", "UserProfile"]


class UserID(Snowflake):
    """
    A :class:`Snowflake` representing a user ID.
    """


class Discriminator(int):
    """
    A :class:`User`'s discriminator. This is the ``#`` of the user.

    This class is an :class:`int`, but there's also helper methods and properties.

    .. traits::
        .. trait:: repr
            The raw discriminator number.
        .. trait:: str
            The formatted or padded discriminator number.
    """

    def __repr__(self) -> str:
        return str(int(self))

    def __str__(self) -> str:
        return f"{int(self):04}"

    @property
    def zero(self) -> bool:
        """
        Returns
        -------
        bool
            If the discriminator is zero.
        """
        return int(self) == 0


class UserFlags(IntFlag):
    """
    A :class:`User`'s flags. This enum contains platform-specific members.

    .. container:: todo
        Finish :ref:`fluxed_up.utils.multiplatform.DependentEnum` and then migrate this enum to that class.
        This raw :class:`IntFlag` is only a temporary solution.
    """

    STAFF = 1 << 0
    DISCORD_PARTNER = 1 << 1
    FLUXER_PARTNER = DISCORD_HYPESQUAD = 1 << 2
    BUG_HUNTER = FLUXER_BUG_HUNTER = DISCORD_BUG_HUNTER_LEVEL_1 = 1 << 3
    FRIENDLY_BOT = 1 << 4
    """Fluxer-specific field"""
    FRIENDLY_BOT_MANUAL_APPROVAL = 1 << 5
    FLUXER_SPAMMER = DISCORD_HYPESQUAD_BRAVERY = 1 << 6
    FLUXER_PROFILE_HIDDEN = DISCORD_HYPESQUAD_BRILLIANCE = 1 << 7
    DISCORD_HYPESQUAD_BALANCE = 1 << 8
    PREMIUM_EARLY_SUPPORTER = 1 << 9
    """Discord-specific field"""
    TEAM_PSEUDO_USER = 1 << 10
    """Discord-specific field"""
    DISCORD_BUG_HUNTER_LEVEL_2 = 1 << 14
    """Discord-specific field"""
    VERIFIED_BOT = 1 << 16
    """Discord-specific field"""
    VERIFIED_DEVELOPER = 1 << 17
    """Discord-specific field"""
    CERTIFIED_MODERATOR = 1 << 18
    """Discord-specific field"""
    BOT_HTTP_INTERACTIONS = 1 << 19
    """Discord-specific field"""


class UserProfile(Model, Protocol):
    """
    Represents a user's profile information.

    The client need to share a mutual guild or be friended with each other to access such information, usually.

    Attributes
    ----------
    id : :class:`UserID`
        The ID of the :class:`User`.
    bio : str
        The bio of the :class:`User`.
    pronouns : str
        The pronouns of the :class:`User`.
    accent_color : :class:`Color`
        The color of the accent of the :class:`User`.
    """

    id: UserID
    bio: str
    pronouns: str
    accent_color: Color


class User(Model, Protocol):
    """
    Represents a user's most basic information on a platform.

    Information like a user's bio, pronouns, and other aspects are not covered by this class.
    Instead, use :class:`UserProfile`.

    .. traits::
        .. trait:: eq
            .. based-on:: ID
        .. trait:: repr
            .. based-on:: ID
        .. trait:: str
            The display name of the User.

    Attributes
    ----------
    id : :class:`UserID`
        The ID of the User.
    username : str
        The User's username. This does not include the discriminator.
    discriminator: Discriminator
        The User's discriminator. This is the ``#`` of the user.
    global_name: str | None
        The User's global name. This value may be ``None``.
    bot: bool
        Whether the User is a bot or not.
    system: bool
        Whether the User is a system user or not.
    flags : :class:`UserFlags`
        The User's flags.
    """

    id: UserID
    username: str
    discriminator: Discriminator
    global_name: str | None
    bot: bool
    system: bool
    flags: UserFlags

    @property
    def display_name(self) -> str:
        """
        Returns
        -------
        str
            The effective display name of the User.
        """
        return self.global_name or self.username

    async def get_dm(self) -> Channel:
        """
        Gets the DM :class:`Channel` with the User.

        |coro|

        Returns
        -------
        :class:`Channel`
            The opened DM with the User.
        """
        raise NotImplementedError
