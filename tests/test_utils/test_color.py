from fluxed_up.utils import Color


def test_construction() -> None:
    assert Color(0xFF00FF)
    assert Color("#FF00FF")
    assert Color(255, 0, 255)
    assert Color(Color("#FF00FF"))


def test_eq() -> None:
    assert (
        Color(0xFF00FF)
        == Color("#FF00FF")
        == Color(255, 0, 255)
        == Color(Color("#FF00FF"))
    )


def test_hash() -> None:
    d: dict[Color, int] = {Color("#FF00FF"): 100, Color(255, 255, 0): 200}
    assert d[Color(255, 0, 255)] == 100
    assert d[Color(0xFFFF00)] == 200


def test_convert() -> None:
    color = Color(0x13579B)
    h, s, v = color.to_hsv()
    from_hsv = Color.from_hsv(h, s, v)
    assert from_hsv.r == color.r and from_hsv.g == color.g and from_hsv.b == color.b
    h, l, s = color.to_hls()
    from_hls = Color.from_hls(h, l, s)
    assert from_hls.r == color.r and from_hls.g == color.g and from_hls.b == color.b
    y, i, q = color.to_yiq()
    from_yiq = Color.from_yiq(y, i, q)
    assert from_yiq.r == color.r and from_yiq.g == color.g and from_yiq.b == color.b


def test_int() -> None:
    raw = 0x13579B
    assert int(Color(raw)) == raw


def test_str() -> None:
    raw = "#13579B"
    assert str(Color(raw)) == raw
