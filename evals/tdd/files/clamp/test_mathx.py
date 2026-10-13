from mathx import clamp


def test_inside_range():
    assert clamp(5, 0, 10) == 5
