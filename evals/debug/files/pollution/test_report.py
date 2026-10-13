from report import render_total


def test_report_total():
    orders = [{"cents": 100000}, {"cents": 23450}]
    assert render_total(orders) == "Total: 1,234.50 EUR"
