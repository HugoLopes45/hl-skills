from decimal import Decimal

from billing import round_total


def test_round_total_whole_cents():
    assert round_total("2.30") == Decimal("2.30")


def test_round_total_half_cent():
    assert round_total("2.345") == Decimal("2.35")
