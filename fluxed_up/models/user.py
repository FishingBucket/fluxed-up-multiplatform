from .snowflake import Snowflake

__all__ = ["Discriminator", "User", "UserID"]


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


class User:
    """
    Represents a user's most basic information on a platform.

    Information like a user's bio, pronouns, and other aspects are not covered by this class.
    Instead, use :class:`UserProfile`.

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
    """

    __slots__ = ("bot", "discriminator", "global_name", "id", "system", "username")

    id: UserID
    username: str
    discriminator: Discriminator
    global_name: str | None
    bot: bool
    system: bool

    @property
    def display_name(self) -> str:
        """
        Returns
        -------
        str
            The effective display name of the user.
        """
        return self.global_name or self.username
