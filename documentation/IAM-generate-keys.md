SECRET_KEY = 2tm1i6sg3lz+&lpq^a*%liaa&aspkwz!a7!7)e8@8vhoz@cf*g

JWT_SECRET_KEY = kh_EBwW5ZCZ7P5YuNnq9qxAU7MtO8-aPOG3o2MODwVZwNvuYGNtLonWZB07GFaPA3Le-F-oHY5wMFTTwRNYCsQ

# secret key

    python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"

# jwt secret key

    python -c "import secrets; print(secrets.token_urlsafe(64))"
