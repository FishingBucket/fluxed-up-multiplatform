from .exceptions import UninitializableResource

__all__ = ["Token"]


class Token:
    """
    An opaque class to wrap an authentication token.
    """

    __slots__ = ("_raw",)

    _raw: str

    def __init__(self) -> None:
        """
        A :class:`Token` class cannot be constructed from user code. This method will always error with :exc:`UninitializableResource`.

        Raises
        ------
        :exc:`UninitializableResource`
            Always.
        """
        raise UninitializableResource("Token")

    def __repr__(self) -> str:
        return "Token(...)"

    def __str__(self) -> str:
        return "Token(...)"

    @classmethod
    def __from_raw(cls, raw: str) -> Token:
        """
        Private method for constructing a new :class:`Token` object from its raw representation.

        Parameters
        ----------
        raw : str
            The raw token underneath.

        Returns
        -------
        :class:`Token`
            The new Token object.
        """
        token = object.__new__(cls)
        token._raw = raw
        return token

    @classmethod
    def from_env(cls, key: str = "TOKEN") -> Token:
        """
        Constructs a :class:`Token` from environmental variables. This method uses the :mod:`dotenv` library if the variable was not loaded.

        This method will check the current environmental variables first before loading from a ``.env`` file.

        Parameters
        ----------
        key : str, optional
            The key of the environmental variable that holds the token. Defaults to ``"TOKEN"``.

        Returns
        -------
        :class:`Token`
            The new :class:`Token` object.

        Raises
        ------
        :exc:`KeyError`
            If the specified key cannot be found.
        """
        import os

        if value := os.environ.get(key):
            return cls.__from_raw(value)

        import dotenv

        dotenv.load_dotenv()
        if value := os.environ.get(key):
            return cls.__from_raw(value)

        raise KeyError(key)

    @classmethod
    def from_string(cls, string: str) -> Token:
        """
        Constructs a :class:`Token` object from its raw representation. This method is not recommended to use in production unless the source token is not visible.

        Parameters
        ----------
        string : str
            The raw token underneath.

        Returns
        -------
        :class:`Token`
            The new :class:`Token` object.
        """
        return cls.__from_raw(string)

    def get_token(self) -> str:
        """
        Gets the raw token string that's being wrapped by this :class:`Token`.

        Returns
        -------
        str
            The raw token underneath.
        """
        return self._raw
