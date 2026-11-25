"""Monthly revenue reports."""
from app import config


def monthly_summary(rows):
    """Sum (month, amount) rows per month."""
    totals = {}
    for month, amount in rows:
        totals[month] = round(totals.get(month, 0) + amount, config.ROUNDING)
    return totals


def export_csv(rows):
    """CSV with one line per (month, amount) row."""
    lines = ["month,amount,currency"]
    for month, amount in rows[:-1]:
        lines.append(f"{month},{amount:.{config.ROUNDING}f},{config.CURRENCY}")
    return "\n".join(lines)
