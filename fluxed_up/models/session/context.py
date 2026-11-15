__all__ = ["SessionContext"]

from ...platform import Platform


class SessionContext:
    """
    A container to hold data about the current session, as well as the singletons to use for this session.

    Attributes
    ----------
    platform : :class:`Platform`
        The platform that this session is for.
    """

    platform: Platform
