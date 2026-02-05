from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed


class IAMAuthentication(JWTAuthentication):
    """
    IAM authentication adapter.

    Supports:
    - Authorization: Bearer <access_token>
    - HttpOnly cookie: access
    """

    cookie_name = "access"

    def authenticate(self, request):
        # 1️⃣ Header-based auth (preferred)
        header = self.get_header(request)
        if header is not None:
            return super().authenticate(request)

        # 2️⃣ Cookie-based auth (browser)
        raw_token = request.COOKIES.get(self.cookie_name)
        if not raw_token:
            return None

        try:
            validated_token = self.get_validated_token(raw_token)
            user = self.get_user(validated_token)
            return user, validated_token
        except Exception as exc:
            raise AuthenticationFailed("Invalid or expired access token") from exc






# from rest_framework_simplejwt.authentication import JWTAuthentication


# from rest_framework_simplejwt.exceptions import InvalidToken, TokenError

# class HybridJWTAuthentication(JWTAuthentication):
#     def authenticate(self, request):
#         header = self.get_header(request)

#         if header:
#             raw_token = self.get_raw_token(header)
#         else:
#             raw_token = request.COOKIES.get("access_token")

#         if not raw_token:
#             return None

#         try:
#             validated_token = self.get_validated_token(raw_token)
#         except (InvalidToken, TokenError):
#             return None   # ← important

#         return self.get_user(validated_token), validated_token

# class HybridJWTAuthentication(JWTAuthentication):
#     def authenticate(self, request):
#         header = self.get_header(request)

#         if header:
#             raw_token = self.get_raw_token(header)
#         else:
#             raw_token = request.COOKIES.get("access_token")

#         if not raw_token:
#             return None

#         validated_token = self.get_validated_token(raw_token)
#         return self.get_user(validated_token), validated_token


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
