# apps/authn/views/logout.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from django.views.decorators.csrf import csrf_protect
from django.utils.decorators import method_decorator

from apps.authn.services.auth_service import logout
from apps.authn.tokens.cookies import clear_auth_cookies


@method_decorator(csrf_protect, name="dispatch")
class LogoutView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request):
        logout(
            refresh_token=request.COOKIES.get("refresh_token"),
        )

        response = Response(
            {"status": "logged out successfully"},
            status=status.HTTP_200_OK,
        )

        clear_auth_cookies(response)
        return response
