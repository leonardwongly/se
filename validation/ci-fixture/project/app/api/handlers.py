"""HTTP-style handlers for the invoice API."""
import uuid

from app.billing import invoice_total
from app.security import require_role, validate_customer_id


def new_request_id():
    return uuid.uuid4().hex[:8]


def handle_invoice(user, customer_id, lines):
    """Entry point for POST /invoice."""
    require_role(user, "billing")
    validate_customer_id(customer_id)
    return {"customer": customer_id, "total": invoice_total(lines), "request_id": new_request_id()}
