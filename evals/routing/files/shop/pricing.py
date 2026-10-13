def total_cents(items):
    return sum(i['cents'] * i['qty'] for i in items)
