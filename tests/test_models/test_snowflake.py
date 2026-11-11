import datetime

import pytest

from fluxed_up import Platform, Snowflake


class SnowflakeA(Snowflake):
    pass


class SnowflakeB(Snowflake):
    pass


def test_direct_construction() -> None:
    with pytest.raises(TypeError):
        Snowflake(100, Platform.Fluxer)


def test_construction() -> None:
    assert SnowflakeA(100, Platform.Fluxer)


def test_equality() -> None:
    assert SnowflakeA(100, Platform.Fluxer) == SnowflakeA(100, Platform.Fluxer)
    assert SnowflakeA(100, Platform.Fluxer) != SnowflakeB(100, Platform.Fluxer)
    assert SnowflakeA(100, Platform.Fluxer) != SnowflakeA(101, Platform.Fluxer)
    assert SnowflakeA(100, Platform.Fluxer) != SnowflakeA(100, Platform.Discord)


def test_hash() -> None:
    d: dict[Snowflake, int] = {
        SnowflakeA(100, Platform.Fluxer): 100,
        SnowflakeB(100, Platform.Fluxer): 200,
        SnowflakeA(100, Platform.Discord): 300,
    }
    assert d[SnowflakeA(100, Platform.Fluxer)] == 100
    assert d[SnowflakeB(100, Platform.Fluxer)] == 200
    assert d[SnowflakeA(100, Platform.Discord)] == 300


def test_ord() -> None:
    a = SnowflakeA(100, Platform.Fluxer)
    b = SnowflakeA(101, Platform.Fluxer)
    assert a < b
    assert b > a
    assert a <= b
    assert b >= a


def test_timestamp() -> None:
    now = datetime.datetime.now().timestamp()
    raw = (int(now * 1000) - Platform.Fluxer.value.epoch_ms) << 22
    snowflake = SnowflakeA(raw, Platform.Fluxer)
    assert snowflake.timestamp == pytest.approx(now)
