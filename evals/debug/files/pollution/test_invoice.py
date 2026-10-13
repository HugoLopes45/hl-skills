from invoice import render


def test_default_invoice():
    assert render([("Widget", 1250)]).endswith("Total: 12.50 EUR")


def test_customer_locale():
    assert render([("Widget", 123450)], locale="de").endswith("Total: 1.234,50 EUR")
