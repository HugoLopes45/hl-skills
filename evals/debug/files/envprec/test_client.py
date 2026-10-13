import pytest

from client import call_with_retries


def test_retries_then_raises():
    calls = []

    def down():
        calls.append(1)
        raise ConnectionError("down")

    with pytest.raises(ConnectionError):
        call_with_retries(down, 2, lambda message: None)
    assert len(calls) == 3
