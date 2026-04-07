import requests
from django.conf import settings


def verify_recaptcha(token: str) -> bool:
    if not token:
        return False
    response = requests.post(
        "https://www.google.com/recaptcha/api/siteverify",
        data={
            "secret": settings.RECAPTCHA_SECRET_KEY,
            "response": token,
        },
        timeout=5,
    )
    return response.json().get("success", False)
