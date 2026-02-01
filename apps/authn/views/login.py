# apps/authn/views/login.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import PermissionDenied

from apps.authn.services.auth_service import login
from apps.authn.tokens.cookies import set_auth_cookies


class LoginView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        try:
            user, tokens = login(
                request=request,
                username=request.data.get("username"),
                password=request.data.get("password"),
            )
        except PermissionDenied:
            return Response(
                {"detail": "Invalid credentials"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        response = Response(
            {"status": "Login successfully"},
            status=status.HTTP_200_OK,
        )

        set_auth_cookies(
            response,
            access=tokens["access"],
            refresh=tokens["refresh"],
        )

        return response
