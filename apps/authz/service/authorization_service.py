# iam/services/authorization.py

from apps.access.models import Permission

class AuthorizationService:

    @staticmethod
    def _load_permissions(user):
        if not hasattr(user, "_cached_permission_codes"):
            user._cached_permission_codes = set(
                Permission.objects.filter(
                    permission_policies__policy__policy_users__user=user
                ).values_list("code", flat=True)
            )
        return user._cached_permission_codes

    @staticmethod
    def has_permission(user, permission_code: str) -> bool:
        if not user.is_active:
            return False
        if user.is_superuser:
            return True

        permissions = AuthorizationService._load_permissions(user)
        return permission_code in permissions

    @staticmethod
    def get_user_permission_codes(user) -> set[str]:
        if not user.is_active:
            return set()
        if user.is_superuser:
            return {"*"}

        return AuthorizationService._load_permissions(user)



# class AuthorizationService:
#     @staticmethod
#     def has_permission(user, permission_code: str) -> bool:
#         if not user.is_active:
#             return False

#         if user.is_superuser:
#             return True

#         return Permission.objects.filter(
#             code=permission_code,
#             permission_policies__policy__policy_users__user=user,
#         ).exists()
