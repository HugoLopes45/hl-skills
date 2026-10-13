TAX = 0.2


def invoice_total(cents):
    return round(cents * (1 + TAX))
