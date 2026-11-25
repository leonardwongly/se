"""Invoice totals."""
from app import config


def _subtotal(lines):
    return sum(quantity * price for quantity, price in lines)


def invoice_total(lines):
    """Total for (quantity, unit price) lines, including tax."""
    return round(_subtotal(lines) * (1 + config.TAX_RATE), config.ROUNDING)
