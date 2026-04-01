

# from rest_framework_simplejwt.authentication import JWTAuthentication
# from rest_framework_simplejwt.exceptions import TokenError
# from rest_framework.exceptions import AuthenticationFailed


# class TokenUser:
#     """Lightweight user object built from JWT claims — no DB lookup."""

#     def __init__(self, token):
#         self.id = token.get("sub")
#         self.username = token.get("username", "")
#         self.is_authenticated = True
#         self.is_active = True
#         self.is_superuser = False  # Inventory never grants superuser locally
#         self.is_anonymous = False

#     def __str__(self):
#         return self.username


# class IAMAuthentication(JWTAuthentication):

#     def authenticate(self, request):
#         raw_token = request.COOKIES.get("access")

#         if raw_token is None:
#             header = self.get_header(request)
#             if header is None:
#                 return None
#             raw_token = self.get_raw_token(header)
#             if raw_token is None:
#                 return None

#         try:
#             validated_token = self.get_validated_token(raw_token)
#         except TokenError as e:
#             raise AuthenticationFailed(str(e))

#         user = TokenUser(validated_token)
#         return user, validated_token

from rest_framework_simplejwt.authentication import JWTStatelessUserAuthentication
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework.exceptions import AuthenticationFailed


class IAMAuthentication(JWTStatelessUserAuthentication):
    """
    Extends simplejwt's built-in stateless auth to also read from HttpOnly cookie.
    Falls back to Bearer header for M2M/Postman.
    """

    def authenticate(self, request):
        raw_token = request.COOKIES.get("access")

        if raw_token is None:
            header = self.get_header(request)
            if header is None:
                return None
            raw_token = self.get_raw_token(header)
            if raw_token is None:
                return None

        try:
            validated_token = self.get_validated_token(raw_token)
        except TokenError as e:
            raise AuthenticationFailed(str(e))

        return self.get_user(validated_token), validated_token
