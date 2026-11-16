import pytest

import client


def test_fetch_gives_up_after_five_attempts():
    calls = []

    def failing():
        calls.append(1)
        raise ConnectionError

    with pytest.raises(ConnectionError):
        client.fetch(failing)
    assert len(calls) == 5
