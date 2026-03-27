from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.exceptions import AuthenticationFailed

from django.views.decorators.csrf import csrf_protect
from django.utils.decorators import method_decorator

from apps.authn.tokens.service import refresh_tokens
from apps.authn.tokens.cookies import (
    set_auth_cookies,
    clear_auth_cookies,
    REFRESH_COOKIE_NAME,
)

from apps.authn.authentication import IAMAuthentication
from apps.audit.services.services import log_action
from apps.audit.models import AuditLog

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
        except AuthenticationFailed:
            log_action(
                action=AuditLog.Action.AUTH_TOKEN_REFRESH,
                status=AuditLog.Status.FAILURE,
                detail={"reason": "Invalid or rotated refresh token"},
                request=request,
            )
            response = Response(status=status.HTTP_401_UNAUTHORIZED)
            clear_auth_cookies(response)
            return response

        actor = None
        try:
            user, _ = IAMAuthentication().authenticate(request)
            actor = user
        except Exception:
            pass

        log_action(
            actor=actor,
            action=AuditLog.Action.AUTH_TOKEN_REFRESH,
            target_id=actor.id if actor else None,
            target_type="user" if actor else "",
            request=request,
        )

        response = Response({"detail": "Token refreshed"}, status=status.HTTP_200_OK)
        set_auth_cookies(response, access=tokens["access"], refresh=tokens["refresh"])
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
