from ledger import monthly_totals


def test_totals():
    assert monthly_totals([{'month': 1, 'amount': 2}]) == {1: 2}
