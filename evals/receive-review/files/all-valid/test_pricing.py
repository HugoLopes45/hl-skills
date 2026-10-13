from pricing import apply_discount, total


def test_total():
    assert total([{"price": 2, "qty": 1}, {"price": 3, "qty": 1}]) == 5


def test_discount():
    assert apply_discount(10, 50) == 5
