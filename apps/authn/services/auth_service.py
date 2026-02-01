# apps/authn/services/auth_service.py

from django.contrib.auth import authenticate
from django.core.exceptions import PermissionDenied
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError

from apps.access.services.permission_resolver import (
    resolve_user_effective_permissions,
)
from apps.authn.tokens.service import issue_user_tokens


def login(*, request, username: str, password: str):
    user = authenticate(
        request,
        username=username,
        password=password,
    )

    if not user:
        raise PermissionDenied("Invalid credentials")

    if not user.is_active:
        raise PermissionDenied("User inactive")

    _, permissions = resolve_user_effective_permissions(user)

    tokens = issue_user_tokens(
        user=user,
        permissions=permissions,
    )

    return user, tokens


def refresh_tokens(*, refresh_token: str):
    if not refresh_token:
        raise PermissionDenied("Refresh token missing")

    try:
        refresh = RefreshToken(refresh_token)
        new_access = refresh.access_token
        new_refresh = str(refresh)
    except TokenError:
        raise PermissionDenied("Invalid or expired refresh token")

    return {
        "access": str(new_access),
        "refresh": new_refresh,
    }

def logout(*, refresh_token: str | None):
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

