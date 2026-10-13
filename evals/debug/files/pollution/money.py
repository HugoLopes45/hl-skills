def format_amount(cents, settings):
    """Format integer cents with the separators in settings."""
    whole, frac = divmod(abs(cents), 100)
    grouped = f"{whole:,}".replace(",", settings["group_sep"])
    sign = "-" if cents < 0 else ""
    return f"{sign}{grouped}{settings['decimal_sep']}{frac:02d} {settings['currency']}"
