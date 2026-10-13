from calc import average, clamp


def test_average():
    assert average([1, 2, 3]) == 2


def test_clamp_inside():
    assert clamp(5, 0, 10) == 5
