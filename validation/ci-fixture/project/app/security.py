"""Input and permission checks for requests reaching the API."""
import re

_CUSTOMER_ID = re.compile(r"^[A-Za-z0-9-]{1,32}$")


def validate_customer_id(value):
    if not isinstance(value, str) or not _CUSTOMER_ID.fullmatch(value):
        raise ValueError("invalid customer id")
    return value


def require_role(user, role):
    if role not in user.get("roles", ()):
        raise PermissionError(f"{role} role required")
