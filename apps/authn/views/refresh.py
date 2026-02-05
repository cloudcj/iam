from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.exceptions import PermissionDenied

from django.views.decorators.csrf import csrf_protect
from django.utils.decorators import method_decorator

from apps.authn.services.auth_service import refresh_tokens
from apps.authn.tokens.cookies import (
    set_auth_cookies,
    clear_auth_cookies,
    REFRESH_COOKIE_NAME,
)


@method_decorator(csrf_protect, name="dispatch")
class RefreshTokenView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request):
        refresh_token = request.COOKIES.get(REFRESH_COOKIE_NAME)

        if not refresh_token:
            response = Response(status=status.HTTP_401_UNAUTHORIZED)
            clear_auth_cookies(response)
            return response

        try:
            tokens = refresh_tokens(refresh_token=refresh_token)
        except PermissionDenied:
            # 🔥 refresh already rotated or invalid
            response = Response(status=status.HTTP_401_UNAUTHORIZED)
            clear_auth_cookies(response)
            return response

        response = Response(
            {"detail": "Token refreshed"},
            status=status.HTTP_200_OK,
        )

        set_auth_cookies(
            response,
            access=tokens["access"],
            refresh=tokens["refresh"],  # REQUIRED with rotation ON
        )

        return response




# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# from rest_framework.permissions import AllowAny
# from django.core.exceptions import PermissionDenied
# from django.views.decorators.csrf import csrf_protect
# from django.utils.decorators import method_decorator

# from apps.authn.services.auth_service import refresh_tokens
# from apps.authn.tokens.cookies import (
#     set_auth_cookies,
#     REFRESH_COOKIE_NAME,
# )

# from django.views.decorators.csrf import csrf_exempt
# from django.utils.decorators import method_decorator

# @method_decorator(csrf_exempt, name="dispatch")
# class RefreshTokenView(APIView):
#     permission_classes = [AllowAny]
#     authentication_classes = []

#     def post(self, request):
#         tokens = refresh_tokens(
#             refresh_token=request.COOKIES.get(REFRESH_COOKIE_NAME),
#         )

#         response = Response(
#             {"detail": "Token refreshed"},
#             status=status.HTTP_200_OK,
#         )

#         set_auth_cookies(
#             response,
#             access=tokens["access"],
#             refresh=tokens["refresh"],
#         )
#         return response
