
import logging

from django.contrib.auth import get_user_model
from django.conf import settings
# from django.core.exceptions import PermissionDenied

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework.exceptions import AuthenticationFailed

from apps.authn.blacklist import blacklist_token,is_blacklisted

logger = logging.getLogger(__name__)

def issue_user_tokens(*, user):
    from apps.authz.services.authorization_service import AuthorizationService

    refresh = RefreshToken.for_user(user)
    access = refresh.access_token

    # ✅ Identity
    access["username"] = user.username
    access["typ"] = "access"
    access["is_superuser"] = user.is_superuser
    access["department"] = user.department.code if user.department else None

    # ✅ Roles (always embedded)
    role_codes = list(user.user_roles.select_related("role").values_list("role__code", flat=True))
    access["roles"] = sorted(role_codes)

    # ✅ Superuser carries empty permissions — bypasses checks locally
    if user.is_superuser:
        access["permissions"] = []
        access["systems"] = []
    else:
        permission_codes = AuthorizationService.get_user_permission_codes(user)
        access["permissions"] = sorted(permission_codes)
        access["systems"] = sorted({
            code.split(".")[0]
            for code in permission_codes
        })

    return {
        "access": str(access),
        "refresh": str(refresh),
    }

def refresh_tokens(*, refresh_token: str):
    from apps.authz.services.authorization_service import AuthorizationService

    if not refresh_token:
        raise AuthenticationFailed("Refresh token missing")

    try:
        old_refresh = RefreshToken(refresh_token)
    except TokenError:
        raise AuthenticationFailed("Invalid or expired refresh token")

    # 🔐 Check if already blacklisted (reuse/replay detection)
    if is_blacklisted(old_refresh["jti"]):
        raise AuthenticationFailed("Invalid or expired refresh token")

    try:
        user_id_claim = settings.SIMPLE_JWT["USER_ID_CLAIM"]
        user_id = old_refresh[user_id_claim]
        user = get_user_model().objects.get(id=user_id)
    except get_user_model().DoesNotExist:
        raise AuthenticationFailed("Invalid or expired refresh token")

    # Blacklist old refresh token in Redis
    blacklist_token(old_refresh["jti"], old_refresh["exp"])

    # Issue a fresh token pair
    new_refresh = RefreshToken.for_user(user)
    new_access = new_refresh.access_token

    # ✅ Identity
    new_access["username"] = user.username
    new_access["typ"] = "access"
    new_access["is_superuser"] = user.is_superuser
    new_access["department"] = user.department.code if user.department else None

    # ✅ Roles (always embedded)
    role_codes = list(user.user_roles.select_related("role").values_list("role__code", flat=True))
    new_access["roles"] = sorted(role_codes)

    # ✅ Re-embed fresh permissions (picks up any changes since last login)
    if user.is_superuser:
        new_access["permissions"] = []
        new_access["systems"] = []
    else:
        permission_codes = AuthorizationService.get_user_permission_codes(user)
        new_access["permissions"] = sorted(permission_codes)
        new_access["systems"] = sorted({
            code.split(".")[0]
            for code in permission_codes
        })

    return {
        "access": str(new_access),
        "refresh": str(new_refresh),
    }


# def issue_user_tokens(*, user):
#     refresh = RefreshToken.for_user(user)
#     access = refresh.access_token

#     # ✅ Identity only — no permissions
#     access["username"] = user.username
#     access["typ"] = "access"

#     return {
#         "access": str(access),
#         "refresh": str(refresh),
#     }


# from apps.authn.blacklist import blacklist_token,is_blacklisted

# def refresh_tokens(*, refresh_token: str):
#     if not refresh_token:
#         raise AuthenticationFailed("Refresh token missing")

#     try:
#         old_refresh = RefreshToken(refresh_token)
#     except TokenError:
#         raise AuthenticationFailed("Invalid or expired refresh token")

#     # 🔐 Check if already blacklisted (reuse/replay detection)
#     if is_blacklisted(old_refresh["jti"]):
#         raise AuthenticationFailed("Invalid or expired refresh token")

#     try:
#         user_id_claim = settings.SIMPLE_JWT["USER_ID_CLAIM"]
#         user_id = old_refresh[user_id_claim]
#         user = get_user_model().objects.get(id=user_id)
#     except get_user_model().DoesNotExist:
#         raise AuthenticationFailed("Invalid or expired refresh token")

#     # Blacklist old refresh token in Redis
#     blacklist_token(old_refresh["jti"], old_refresh["exp"])

#     # Issue a fresh token pair (proper rotation)
#     new_refresh = RefreshToken.for_user(user)
#     new_access = new_refresh.access_token
#     new_access["username"] = user.username
#     new_access["typ"] = "access"

#     return {
#         "access": str(new_access),
#         "refresh": str(new_refresh),
#     }
# def revoke_tokens(refresh_token):
#     blacklist_token(refresh_token["jti"], refresh_token["exp"])

