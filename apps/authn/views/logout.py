# apps/authn/views/logout.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from django.views.decorators.csrf import csrf_protect
from django.utils.decorators import method_decorator

from apps.authn.services.auth_service import logout
from apps.authn.tokens.cookies import (
    clear_auth_cookies,
    REFRESH_COOKIE_NAME,
)

from apps.authn.authentication import IAMAuthentication
from apps.audit.services.services import log_action
from apps.audit.models import AuditLog


@method_decorator(csrf_protect, name="dispatch")
class LogoutView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request):
        actor = None
        try:
            user, _ = IAMAuthentication().authenticate(request)
            actor = user
        except Exception:
            pass

        logout(refresh_token=request.COOKIES.get(REFRESH_COOKIE_NAME))

        log_action(
            actor=actor,
            action=AuditLog.Action.AUTH_LOGOUT,
            target_id=actor.id if actor else None,
            target_type="user" if actor else "",
            detail={"username": actor.username if actor else "unknown"},
            request=request,
        )

        response = Response({"status": "logged out successfully"}, status=status.HTTP_200_OK)
        clear_auth_cookies(response)
        return response
