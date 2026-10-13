from shop.pagination import page


def test_first_item():
    assert page(list(range(10)), 0, 5)[0] == 0
