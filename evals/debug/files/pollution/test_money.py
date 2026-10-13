from money import format_amount

EN = {"decimal_sep": ".", "group_sep": ",", "currency": "EUR"}


def test_negative():
    assert format_amount(-5, EN) == "-0.05 EUR"


def test_grouping():
    assert format_amount(123456789, EN) == "1,234,567.89 EUR"
