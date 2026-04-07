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
from apps.authn.throttles import LoginRateThrottle

from apps.audit.services.services import log_action
from apps.audit.models import AuditLog

from apps.authn.recaptcha import verify_recaptcha

@method_decorator(ensure_csrf_cookie, name="dispatch")
class LoginView(APIView):
    authentication_classes = []
    permission_classes = []
    throttle_classes = [LoginRateThrottle]   # ← add this line

    def post(self, request):
        username = request.data.get("username", "")

        recaptcha_token = request.data.get("recaptcha_token", "")
        if not verify_recaptcha(recaptcha_token):
            return Response(
                {"detail": "reCAPTCHA verification failed. Please try again."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            user, tokens = login(
                request=request,
                username=username,
                password=request.data.get("password"),
            )
        except PermissionDenied as exc:
            log_action(
                action=AuditLog.Action.AUTH_LOGIN_FAILED,
                status=AuditLog.Status.FAILURE,
                detail={"username": username, "reason": str(exc)},
                request=request,
            )
            return Response({"detail": str(exc)}, status=status.HTTP_401_UNAUTHORIZED)

        log_action(
            actor=user,
            action=AuditLog.Action.AUTH_LOGIN,
            target_id=user.id,
            target_type="user",
            detail={"username": user.username},
            request=request,
        )

        response = Response(
            {
                "detail": "Login successful",
                "must_change_password": user.must_change_password,
            },
            status=status.HTTP_200_OK,
        )
        set_auth_cookies(response, access=tokens["access"], refresh=tokens["refresh"])
        return response

