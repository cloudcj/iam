# from rest_framework_simplejwt.authentication import JWTAuthentication
# from rest_framework.exceptions import AuthenticationFailed


# class IAMAuthentication(JWTAuthentication):
#     """
#     IAM authentication adapter.

#     Supports:
#     - Authorization: Bearer <access_token>
#     - HttpOnly cookie: access
#     """

#     cookie_name = "access"

#     def authenticate(self, request):
#         # 1️⃣ Header-based auth (preferred)
#         header = self.get_header(request)
#         if header is not None:
#             return super().authenticate(request)

#         # 2️⃣ Cookie-based auth (browser)
#         raw_token = request.COOKIES.get(self.cookie_name)
#         if not raw_token:
#             return None

#         try:
#             validated_token = self.get_validated_token(raw_token)
#             user = self.get_user(validated_token)
#             return user, validated_token
#         except Exception as exc:
#             raise AuthenticationFailed("Invalid or expired access token") from exc

import logging
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from apps.authn.blacklist.service import is_blacklisted

logger = logging.getLogger(__name__)

class IAMAuthentication(JWTAuthentication):
    cookie_name = "access"

    def authenticate(self, request):
        # 1. Try header first (machine-to-machine calls)
        header = self.get_header(request)
        if header is not None:
            return super().authenticate(request)

        # 2. Try cookie (browser)
        raw_token = request.COOKIES.get(self.cookie_name)
        if not raw_token:
            return None  # No credentials at all — let Django handle as anonymous

        # FIX: catch specific exceptions, not bare Exception
        # Before: except Exception — hid real server errors
        # Now: only catch token-specific errors, real errors still surface
        try:
            validated_token = self.get_validated_token(raw_token)
            user = self.get_user(validated_token)
            return user, validated_token
        except (InvalidToken, TokenError) as exc:
            raise AuthenticationFailed("Invalid or expired access token") from exc


    def get_validated_token(self, raw_token):
        token = super().get_validated_token(raw_token)
        jti = token.get("jti")
        if jti and is_blacklisted(jti):
            raise InvalidToken("Token has been revoked")
        return token


# class IAMAuthentication(JWTAuthentication):
#     """
#     Supports both:
#     - Authorization: Bearer <token>  (machine-to-machine)
#     - HttpOnly cookie: access        (browser)
#     """
#     cookie_name = "access"

#     def authenticate(self, request):
#         # 1. Try header first (machine-to-machine calls)
#         header = self.get_header(request)
#         if header is not None:
#             return super().authenticate(request)

#         # 2. Try cookie (browser)
#         raw_token = request.COOKIES.get(self.cookie_name)
#         if not raw_token:
#             return None  # No credentials at all — let Django handle as anonymous

#         # FIX: catch specific exceptions, not bare Exception
#         # Before: except Exception — hid real server errors
#         # Now: only catch token-specific errors, real errors still surface
#         try:
#             validated_token = self.get_validated_token(raw_token)
#             user = self.get_user(validated_token)
#             return user, validated_token
#         except (InvalidToken, TokenError) as exc:
#             raise AuthenticationFailed("Invalid or expired access token") from exc



###############################################

from django.contrib.auth import authenticate
from rest_framework.exceptions import AuthenticationFailed


def authenticate_user(*, request=None, username, password):
    """
    Authenticate user credentials.
    identity-only. No JWT logic here.
    """

    user = authenticate(
        request,
        username=username,
        password=password,
    )

    if not user:
        raise AuthenticationFailed("Invalid username or password")

    if not user.is_active:
        raise AuthenticationFailed("User is inactive")

    return user
