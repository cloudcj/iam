# common/auth/jwt.py (inventory / monitoring / ticketing)

import jwt
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.conf import settings

class ServiceJWTAuthentication(BaseAuthentication):
"""
Stateless JWT authentication for microservices.
Trusts GAIA IAM as issuer.
"""

    def authenticate(self, request):
        token = self._get_token(request)
        if not token:
            return None

        try:
            payload = jwt.decode(
                token,
                settings.IAM_PUBLIC_KEY,
                algorithms=["RS256"],
                issuer="gaia-iam",
                audience="gaia-api",
                options={
                    "require": ["exp", "iat", "sub"],
                },
            )
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Token expired")
        except jwt.InvalidTokenError:
            raise AuthenticationFailed("Invalid token")

        # No DB lookup — token is the source of truth
        return (payload, payload)

    def _get_token(self, request):
        auth = request.headers.get("Authorization")
        if not auth:
            return None

        try:
            scheme, token = auth.split()
            if scheme.lower() != "bearer":
                return None
            return token
        except ValueError:
            return None
