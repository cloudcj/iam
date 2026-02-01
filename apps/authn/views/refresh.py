# apps/authn/views/refresh.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from django.core.exceptions import PermissionDenied
from django.views.decorators.csrf import csrf_protect
from django.utils.decorators import method_decorator

from apps.authn.services.auth_service import refresh_tokens
from apps.authn.tokens.cookies import set_auth_cookies


@method_decorator(csrf_protect, name="dispatch")
class RefreshTokenView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request):
        try:
            tokens = refresh_tokens(
                refresh_token=request.COOKIES.get("refresh_token"),
            )
        except PermissionDenied as exc:
            return Response(
                {"detail": str(exc)},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        response = Response({"status": "refreshed"})
        set_auth_cookies(
            response,
            access=tokens["access"],
            refresh=tokens["refresh"],
        )
        return response
