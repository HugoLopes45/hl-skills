import report


def test_total():
    assert report.total([{"amount": 2}, {"amount": 3}]) == 5
