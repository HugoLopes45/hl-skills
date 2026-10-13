TAX = 0.2


def quote_total(cents):
    return int(cents * (1 + TAX))
