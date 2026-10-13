def monthly_totals(rows):
    totals = {}
    for r in rows:
        totals[r['month']] = totals.get(r['month'], 0) + r['amount']
    return totals
