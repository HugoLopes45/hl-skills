from invoice import invoice_total
from quote import quote_total


def test_invoice_total():
    assert invoice_total(1000) == 1200


def test_quote_total():
    assert quote_total(1000) == 1200
