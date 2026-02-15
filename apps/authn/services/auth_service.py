from django.contrib.auth import authenticate, get_user_model
from django.core.exceptions import PermissionDenied
from apps.access.services.permission_resolver import (
    resolve_user_effective_permissions,
)
from apps.authn.tokens.service import issue_user_tokens

User = get_user_model()


def login(*, request, username: str, password: str):
    try:
        user_obj = User.objects.get(username=username)
    except User.DoesNotExist:
        raise PermissionDenied("Invalid credentials")

    if not user_obj.is_active:
        raise PermissionDenied("Account is deactivated")

    user = authenticate(
        request=request,
        username=username,
        password=password,
    )

    if not user:
        raise PermissionDenied("Invalid credentials")

    tokens = issue_user_tokens(user=user)

    return user, tokens




from django.core.exceptions import PermissionDenied
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError

from django.contrib.auth import get_user_model
from django.core.exceptions import PermissionDenied
from rest_framework_simplejwt.tokens import RefreshToken, TokenError

from apps.access.services.permission_resolver import (
    resolve_user_effective_permissions,
)
from django.conf import settings



def refresh_tokens(*, refresh_token: str):
    if not refresh_token:
        raise PermissionDenied("Refresh token missing")

    try:
        refresh = RefreshToken(refresh_token)

        user_id_claim = settings.SIMPLE_JWT["USER_ID_CLAIM"]
        user_id = refresh[user_id_claim]

        user = get_user_model().objects.get(id=user_id)
    except Exception:
        raise PermissionDenied("Invalid or expired refresh token")

    _, permissions = resolve_user_effective_permissions(user)

    access = refresh.access_token
    access["permissions"] = permissions
    access["username"] = user.username
    access["typ"] = "access"

    return {
        "access": str(access),
        "refresh": str(refresh),
    }

# def refresh_tokens(*, refresh_token: str):
#     if not refresh_token:
#         raise PermissionDenied("Refresh token missing")

#     try:
#         refresh = RefreshToken(refresh_token)
#     except TokenError:
#         raise PermissionDenied("Invalid or expired refresh token")

#     # SimpleJWT handles:
#     # - validation
#     # - rotation
#     # - blacklisting (if enabled)
#     new_access = refresh.access_token
#     new_refresh = str(refresh)

#     return {
#         "access": str(new_access),
#         "refresh": new_refresh,
    # }

def logout_user(*, refresh_token: str | None):
    """
    Invalidate refresh token if present.
    Safe to call multiple times.
    """
    if not refresh_token:
        return

    try:
        token = RefreshToken(refresh_token)
        token.blacklist()
    except TokenError:
        # already invalid / expired → noop
        pass















# # apps/authn/services/auth_service.py

# from django.contrib.auth import authenticate
# from django.core.exceptions import PermissionDenied

# from apps.access.services.permission_resolver import (
#     resolve_user_roles_and_permissions,
# )
# from apps.authn.tokens.service import issue_user_tokens
# from apps.audit.services.audit_logger import log_event


# def login(*, request, username: str, password: str):
#     user = authenticate(
#         request,
#         username=username,
#         password=password,
#     )

#     if not user:
#         log_event(
#             action="LOGIN_FAILED",
#             request=request,
#             metadata={"reason": "invalid_credentials"},
#         )
#         raise PermissionDenied("Invalid credentials")

#     if not user.is_active:
#         log_event(
#             action="LOGIN_FAILED",
#             user=user,
#             request=request,
#             metadata={"reason": "inactive_user"},
#         )
#         raise PermissionDenied("User inactive")

#     roles, permissions = resolve_user_roles_and_permissions(user)

#     tokens = issue_user_tokens(
#         user=user,
#         permissions=permissions,
#     )

#     log_event(
#         action="LOGIN_SUCCESS",
#         user=user,
#         request=request,
#     )

#     return user, tokens



# # apps/authn/services/auth_service.py

# from rest_framework_simplejwt.tokens import RefreshToken
# from rest_framework_simplejwt.exceptions import TokenError
# from django.core.exceptions import PermissionDenied

# from apps.audit.services.audit_logger import log_event


# def refresh_tokens(*, request, refresh_token: str):
#     if not refresh_token:
#         raise PermissionDenied("Refresh token missing")

#     try:
#         refresh = RefreshToken(refresh_token)
#         new_access = refresh.access_token

#         # NOTE: refresh rotation depends on SIMPLE_JWT settings
#         new_refresh = str(refresh)

#     except TokenError:
#         log_event(
#             action="TOKEN_REFRESH_FAILED",
#             request=request,
#         )
#         raise PermissionDenied("Invalid or expired refresh token")

#     log_event(
#         action="TOKEN_REFRESH",
#         request=request,
#     )

#     return {
#         "access": str(new_access),
#         "refresh": new_refresh,
#     }

