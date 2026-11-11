import os

import pytest

from fluxed_up import Token, exceptions

EXAMPLE_TOKEN = "EXAMPLE_TOKEN"


def test_token_init() -> None:
    with pytest.raises(exceptions.UninitializableResource):
        Token()


def test_from_env() -> None:
    os.environ["TOKEN"] = EXAMPLE_TOKEN
    token = Token.from_env()
    assert token.get_token() == EXAMPLE_TOKEN


def test_from_env_file() -> None:
    token = Token.from_env()
    assert token.get_token() == EXAMPLE_TOKEN


def test_from_string() -> None:
    token = Token.from_string(EXAMPLE_TOKEN)
    assert token.get_token() == EXAMPLE_TOKEN
