import jwt
from django.conf import settings
from rest_framework.exceptions import AuthenticationFailed

from .jwks import get_public_key


def verify_access_token(token: str) -> dict:
    # 1. Read header (unverified)
    try:
        header = jwt.get_unverified_header(token)
    except jwt.InvalidTokenError:
        raise AuthenticationFailed("Invalid JWT header")

    kid = header.get("kid")
    if not kid:
        raise AuthenticationFailed("Missing kid")

    # 2. Resolve correct public key via JWKS
    public_key = get_public_key(kid)

    # 3. Verify signature + registered claims
    try:
        payload = jwt.decode(
            token,
            public_key,
            algorithms=["RS256"],
            issuer=settings.JWT_ISSUER,
            audience=settings.JWT_AUDIENCE,
            leeway=30,  # clock skew tolerance
        )
    except jwt.ExpiredSignatureError:
        raise AuthenticationFailed("Token expired")
    except jwt.InvalidAudienceError:
        raise AuthenticationFailed("Invalid audience")
    except jwt.InvalidIssuerError:
        raise AuthenticationFailed("Invalid issuer")
    except jwt.InvalidTokenError:
        raise AuthenticationFailed("Invalid token")

    return payload