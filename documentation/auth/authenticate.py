# from rest_framework.authentication import BaseAuthentication
# from rest_framework.exceptions import AuthenticationFailed
# from django.contrib.auth.models import AnonymousUser
# from .verify import verify_access_token


# class JWKSJWTAuthentication(BaseAuthentication):
#     def authenticate(self, request):
#         auth = request.headers.get("Authorization")

#         if not auth or not auth.startswith("Bearer "):
#             return None  # DRF will treat as unauthenticated

#         token = auth.split(" ", 1)[1]

#         try:
#             claims = verify_access_token(token)
#         except Exception as e:
#             raise AuthenticationFailed(str(e))

#         # We don’t load a Django user from DB
#         user = AnonymousUser()

#         # DRF convention: (user, auth)
#         return (user, claims)


import jwt

from django.conf import settings
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed

# class IAMCookieJWTAuthentication(BaseAuthentication):
#     """
#     Authenticates IAM-issued JWTs from HttpOnly cookies.
#     """

#     def authenticate(self, request):
#         token = request.COOKIES.get("access")
#         if not token:
#             return None  # DRF will handle unauthenticated case

#         try:
#             claims = jwt.decode(
#                 token,
#                 settings.JWT_PUBLIC_KEY,
#                 algorithms=["RS256"],
#                 issuer=settings.JWT_ISSUER,
#                 audience=settings.JWT_AUDIENCE,
#             )
#         except jwt.ExpiredSignatureError:
#             raise AuthenticationFailed("Access token expired")
#         except jwt.InvalidTokenError:
#             raise AuthenticationFailed("Invalid access token")

#         # Structural validation
#         if not claims.get("sub", "").startswith("user:"):
#             raise AuthenticationFailed("Invalid token subject")

#         # Return (user, auth)
#         # We don’t resolve a Django user in services
#         return None, claims

from .models import JWTUser

class IAMCookieJWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        token = request.COOKIES.get("access")
        if not token:
            return None

        try:
            claims = jwt.decode(
                token,
                settings.JWT_PUBLIC_KEY,
                algorithms=["RS256"],
                issuer=settings.JWT_ISSUER,
                audience=settings.JWT_AUDIENCE,
            )
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Access token expired")
        except jwt.InvalidTokenError:
            raise AuthenticationFailed("Invalid access token")

        sub = claims.get("sub")
        if not sub:
            raise AuthenticationFailed("Missing token subject")

        user = JWTUser(
            user_id=sub,
            username=claims.get("username"),
        )

        return user, claims
