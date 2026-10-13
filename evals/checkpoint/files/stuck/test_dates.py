from datetime import date

from dates import parse_date


def test_parses_iso_timestamp_from_api():
    assert parse_date("2024-03-05T10:00:00Z") == date(2024, 3, 5)
