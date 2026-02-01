from rest_framework_simplejwt.authentication import JWTAuthentication

# class CookieJWTAuthentication(JWTAuthentication):
#     def authenticate(self, request):
#         raw_token = request.COOKIES.get("access_token")

#         if raw_token is None:
#             return None

#         validated_token = self.get_validated_token(raw_token)
#         return self.get_user(validated_token), validated_token


class HybridJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        header = self.get_header(request)

        if header:
            raw_token = self.get_raw_token(header)
        else:
            raw_token = request.COOKIES.get("access_token")

        if not raw_token:
            return None

        validated_token = self.get_validated_token(raw_token)
        return self.get_user(validated_token), validated_token


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
