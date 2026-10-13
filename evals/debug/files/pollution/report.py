from money import format_amount
from settings import get_settings


def render_total(orders):
    """Internal revenue report, always in the company locale."""
    total = sum(order["cents"] for order in orders)
    return f"Total: {format_amount(total, get_settings())}"
