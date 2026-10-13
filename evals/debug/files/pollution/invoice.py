from money import format_amount
from settings import get_settings

LOCALES = {
    "en": {"decimal_sep": ".", "group_sep": ","},
    "de": {"decimal_sep": ",", "group_sep": "."},
    "fr": {"decimal_sep": ",", "group_sep": " "},
}


def render(lines, locale=None):
    """Render invoice lines, optionally in the customer's locale."""
    settings = get_settings()
    if locale:
        settings.update(LOCALES[locale], locale=locale)
    rows = [f"{label}: {format_amount(cents, settings)}" for label, cents in lines]
    total = sum(cents for _, cents in lines)
    rows.append(f"Total: {format_amount(total, settings)}")
    return "\n".join(rows)
