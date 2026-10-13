from pricing import total


def test_small_order_has_no_discount():
    assert total([10, 10]) == 20


def test_three_items_get_discount():
    assert total([10, 10, 10]) == 27.0
