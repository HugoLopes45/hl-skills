from functools import lru_cache


@lru_cache(maxsize=None)
def get_settings():
    """Load the process-wide settings once."""
    return {"locale": "en", "currency": "EUR", "decimal_sep": ".", "group_sep": ","}
