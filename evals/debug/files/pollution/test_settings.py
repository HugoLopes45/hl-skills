from settings import get_settings


def test_defaults():
    assert get_settings()["currency"] == "EUR"
