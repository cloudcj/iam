# # apps/authn/views/login.py

# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# from django.core.exceptions import PermissionDenied

# from apps.authn.services.auth_service import login
# from apps.authn.tokens.cookies import set_auth_cookies

# from django.views.decorators.csrf import ensure_csrf_cookie
# from django.utils.decorators import method_decorator


# @method_decorator(ensure_csrf_cookie, name="dispatch")
# class LoginView(APIView):
#     authentication_classes = []
#     permission_classes = []

#     def post(self, request):
#         try:
#             user, tokens = login(
#                 request=request,
#                 username=request.data.get("username"),
#                 password=request.data.get("password"),
#             )
#         except PermissionDenied:
#             return Response(
#                 {"detail": "Invalid credentials"},
#                 status=status.HTTP_401_UNAUTHORIZED,
#             )

#         response = Response(
#             {"detail": "Login successful"},
#             status=status.HTTP_200_OK,
#         )

#         set_auth_cookies(
#             response,
#             access=tokens["access"],
#             refresh=tokens["refresh"],
#         )

#         return response

from django.core.exceptions import PermissionDenied
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie

from apps.authn.services.auth_service import login
from apps.authn.tokens.cookies import set_auth_cookies


@method_decorator(ensure_csrf_cookie, name="dispatch")
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
        except PermissionDenied as exc:
            return Response(
                {"detail": str(exc)},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        response = Response(
            {"detail": "Login successful"},
            status=status.HTTP_200_OK,
        )

        set_auth_cookies(
            response,
            access=tokens["access"],
            refresh=tokens["refresh"],
        )

        return response
