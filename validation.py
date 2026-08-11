import re

EMAIL_RE = re.compile(r"^[^\s@]+@[^\s@]+\.[^\s@]+$")

VALID_SERVICES = {
    "Grant Proposal Writing",
    "Business Plan Writing",
    "Marketing Copywriting",
    "Data Analysis & Modelling",
    "Web Development & UI/UX Design",
    "Graphic Design",
    "Field Data Collection",
    "Other",
}

MAX_LENGTHS = {
    "name": 150,
    "email": 200,
    "phone": 30,
    "service": 60,
    "message": 5000,
    "page": 500,
}


class ValidationError(Exception):
    def __init__(self, message: str, field: str = None):
        super().__init__(message)
        self.field = field


def _clean(value) -> str:
    return str(value).strip() if value is not None else ""


def validate_submission(payload: dict) -> dict:
    name = _clean(payload.get("name"))
    email = _clean(payload.get("email"))
    phone = _clean(payload.get("phone"))
    service = _clean(payload.get("service")) or "Other"
    message = _clean(payload.get("message"))
    page = _clean(payload.get("page"))

    if not name:
        raise ValidationError("Please enter your full name.", field="name")
    if len(name) > MAX_LENGTHS["name"]:
        raise ValidationError("Name is too long.", field="name")

    if not email:
        raise ValidationError("Please enter your email address.", field="email")
    if not EMAIL_RE.match(email) or len(email) > MAX_LENGTHS["email"]:
        raise ValidationError("Please enter a valid email address.", field="email")

    if phone and len(phone) > MAX_LENGTHS["phone"]:
        raise ValidationError("Phone number is too long.", field="phone")

    if service not in VALID_SERVICES:
        service = "Other"

    if not message:
        raise ValidationError("Please describe your project.", field="message")
    if len(message) > MAX_LENGTHS["message"]:
        raise ValidationError("Message is too long (max 5000 characters).", field="message")

    if len(page) > MAX_LENGTHS["page"]:
        page = page[: MAX_LENGTHS["page"]]

    return {
        "name": name,
        "email": email,
        "phone": phone,
        "service": service,
        "message": message,
        "page": page,
    }
