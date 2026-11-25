__all__ = ["Intents"]

from enum import IntFlag
from functools import reduce


class Intents(IntFlag):
    """
    The flags representing a client's intents.
    """

    GUILDS = 1 << 0
    GUILD_MEMBERS = 1 << 1
    GUILD_MODERATION = 1 << 2
    GUILD_EXPRESSIONS = 1 << 3
    GUILD_INTEGRATIONS = 1 << 4
    GUILD_WEBHOOKS = 1 << 5
    GUILD_INVITES = 1 << 6
    GUILD_VOICE_STATES = 1 << 7
    GUILD_PRESENCES = 1 << 8
    GUILD_MESSAGES = 1 << 9
    GUILD_MESSAGE_REACTIONS = 1 << 10
    GUILD_MESSAGE_TYPING = 1 << 11
    DIRECT_MESSAGES = 1 << 12
    DIRECT_MESSAGE_REACTIONS = 1 << 13
    DIRECT_MESSAGE_TYPING = 1 << 14
    MESSAGE_CONTENT = 1 << 15
    GUILD_SCHEDULED_EVENTS = 1 << 16
    AUTO_MODERATION_CONFIGURATION = 1 << 20
    AUTO_MODERATION_EXECUTION = 1 << 21
    GUILD_MESSAGE_POLLS = 1 << 24
    DIRECT_MESSAGE_POLLS = 1 << 25

    @classmethod
    def default(cls) -> Intents:
        """
        Gets the default intents with "privileged" intents disabled.
        """
        all = cls.all()
        all &= ~cls.GUILD_PRESENCES
        all &= ~cls.GUILD_MEMBERS
        all &= ~cls.MESSAGE_CONTENT
        return all

    @classmethod
    def all(cls) -> Intents:
        """
        Gets all intents.
        """
        return cls(reduce(lambda a, b: a | b, cls))
