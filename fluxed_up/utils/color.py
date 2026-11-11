__all__ = ["Color"]

import colorsys
from typing import overload


def _deconstruct_hex_int(hex_int: int) -> tuple[int, int, int]:
    r = (hex_int >> 16) & 0xFF
    g = (hex_int >> 8) & 0xFF
    b = hex_int & 0xFF
    return r, g, b


def _deconstruct_hex_string(hex_string: str) -> tuple[int, int, int]:
    as_int = int(hex_string, 16)
    return _deconstruct_hex_int(as_int)


def _component_round(v: float) -> int:
    return max(min(round(v), 255), 0)


class Color:
    """
    Represents a color composed of red, green, and blue components.

    This class is purposefully bare as it is a utility class.
    Also provides some convenience methods around `colorsys <https://docs.python.org/3/library/colorsys.html>`_.

    .. traits::
        .. trait:: eq
            .. based-on:: r, g, b
        .. trait:: hash
            .. based-on:: r, g, b
        .. trait:: repr
            .. type:: construction
        .. trait:: str
            Returns the color as a #RRGGBB string.
        .. trait:: int
            Returns the color as a 24-bit integer.

    Attributes
    ----------
    r : int
        The red component of the color as a number between 0 and 255.
    g : int
        The green component of the color as a number between 0 and 255.
    b : int
        The blue component of the color as a number between 0 and 255.

    Examples
    --------
    A Color can be created in many ways. The following are all equivalent:

    >>> Color(0xFF00FF)    ==
    ... Color(255, 0, 255) ==
    ... Color("#ff00ff")   ==
    ... Color(Color(0xFF00FF))
    True
    """

    __slots__ = ("b", "g", "r")

    r: int
    g: int
    b: int

    @overload
    def __init__(self, integer: int, /) -> None:
        """
        Create a new Color from its 24-bit integer representation.

        Parameters
        ----------
        integer : int
            An integer between ``0x000000`` and ``0xFFFFFF``.
        """

    @overload
    def __init__(self, string: str, /) -> None:
        """
        Creates a new Color from its hex code representation.

        Parameters
        ----------
        string : str
            A string in the form of ``"#RRGGBB"``.
        """

    @overload
    def __init__(self, r: int, g: int, b: int, /) -> None:
        """
        Creates a new Color from its three components.

        Parameters
        ----------
        r : int
            The red component of the color as a number between 0 and 255.
        g : int
            The green component of the color as a number between 0 and 255.
        b : int
            The blue component of the color as a number between 0 and 255.
        """

    @overload
    def __init__(self, color: Color, /) -> None:
        """
        Creates a new Color from another Color.

        Parameters
        ----------
        color : Color
            The color to copy from.
        """

    def __init__(
        self,
        arg1: int | str | Color,
        arg2: int | None = None,
        arg3: int | None = None,
        /,
    ) -> None:
        if arg2 is not None and arg3 is None:
            raise TypeError(
                '"Color" cannot be called with 2 arguments. The possible invocations are '
                '"Color(0xFF00FF)", "Color(\'0xFF00FF\')", "Color(255, 0, 255)", or "Color(color)".'
            )

        if isinstance(arg1, Color):
            self.r, self.g, self.b = arg1.r, arg1.g, arg1.b
        elif isinstance(arg1, str):
            if arg1.startswith("#"):
                self.r, self.g, self.b = _deconstruct_hex_string(arg1[1:])
            else:
                self.r, self.g, self.b = _deconstruct_hex_string(arg1)
        elif isinstance(arg1, int):
            if arg2 is not None and arg3 is not None:
                self.r, self.g, self.b = arg1, arg2, arg3
            else:
                self.r, self.g, self.b = _deconstruct_hex_int(arg1)

    def __eq__(self, other: object) -> bool:
        return (
            isinstance(other, Color)
            and self.r == other.r
            and self.g == other.g
            and self.b == other.b
        )

    def __hash__(self) -> int:
        return hash((self.r, self.g, self.b))

    def __repr__(self) -> str:
        return f"Color({self.r}, {self.g}, {self.b})"

    def __str__(self) -> str:
        return f"#{int(self):06X}"

    def __int__(self) -> int:
        return (self.r << 16) + (self.g << 8) + self.b

    @property
    def norm_r(self) -> float:
        """
        Returns
        -------
        float
            The red value of the Color normalized to the ``0.0`` to ``1.0`` range.
        """
        return self.r / 255

    @property
    def norm_g(self) -> float:
        """
        Returns
        -------
        float
            The green value of the Color normalized to the ``0.0`` to ``1.0`` range.
        """
        return self.g / 255

    @property
    def norm_b(self) -> float:
        """
        Returns
        -------
        float
            The blue value of the Color normalized to the ``0.0`` to ``1.0`` range.
        """
        return self.b / 255

    def to_yiq(self) -> tuple[float, float, float]:
        """
        Converts the Color to YIQ coordinates.

        |colorsys|

        Returns
        -------
        tuple[float, float, float]
            The converted YIQ coordinates.
        """
        return colorsys.rgb_to_yiq(self.norm_r, self.norm_g, self.norm_b)

    @classmethod
    def from_yiq(cls, y: float, i: float, q: float) -> Color:
        """
        Creates a Color from its YIQ coordinates.

        |colorsys|

        Parameters
        ----------
        y : float
            The Y component from ``0.0`` to ``1.0``.
        i : float
            The I component.
        q : float
            The Q component.

        Returns
        -------
        Color
            The constructed Color.
        """
        norm_r, norm_g, norm_b = colorsys.yiq_to_rgb(y, i, q)
        return cls(
            _component_round(norm_r * 255),
            _component_round(norm_g * 255),
            _component_round(norm_b * 255),
        )

    def to_hls(self) -> tuple[float, float, float]:
        """
        Converts the Color to HLS coordinates.

        |colorsys|

        Returns
        -------
        tuple[float, float, float]
            The converted HLS coordinates.
        """
        return colorsys.rgb_to_hls(self.norm_r, self.norm_g, self.norm_b)

    @classmethod
    def from_hls(cls, h: float, l: float, s: float) -> Color:
        """
        Creates a Color from its HLS coordinates.

        |colorsys|

        Parameters
        ----------
        h : float
            The hue component from ``0.0`` to ``1.0``.
        l : float
            The lightness component from ``0.0`` to ``1.0``.
        s : float
            The saturation component from ``0.0`` to ``1.0``.

        Returns
        -------
        Color
            The constructed Color.
        """
        norm_r, norm_g, norm_b = colorsys.hls_to_rgb(h, l, s)
        return cls(
            _component_round(norm_r * 255),
            _component_round(norm_g * 255),
            _component_round(norm_b * 255),
        )

    def to_hsv(self) -> tuple[float, float, float]:
        """
        Converts the Color to HSV coordinates.

        |colorsys|

        Returns
        -------
        tuple[float, float, float]
            The converted HSV coordinates.
        """
        return colorsys.rgb_to_hsv(self.norm_r, self.norm_g, self.norm_b)

    @classmethod
    def from_hsv(cls, h: float, s: float, v: float) -> Color:
        """
        Creates a Color from its HSV coordinates.

        |colorsys|

        Parameters
        ----------
        h : float
            The hue component from ``0.0`` to ``1.0``.
        s : float
            The saturation component from ``0.0`` to ``1.0``.
        v : float
            The value component from ``0.0`` to ``1.0``.

        Returns
        -------
        Color
            The constructed Color.
        """
        norm_r, norm_g, norm_b = colorsys.hsv_to_rgb(h, s, v)
        return cls(
            _component_round(norm_r * 255),
            _component_round(norm_g * 255),
            _component_round(norm_b * 255),
        )
