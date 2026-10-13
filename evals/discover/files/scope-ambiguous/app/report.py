from app import store
from app.sync import push

_cache = {}


def invalidate():
    _cache.clear()


def monthly():
    if "monthly" not in _cache:
        totals = {}
        for month, amount in store.load_rows():
            totals[month] = totals.get(month, 0) + amount
        _cache["monthly"] = totals
        push(totals)
    return _cache["monthly"]
