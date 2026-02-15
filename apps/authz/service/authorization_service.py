# iam/services/authorization.py

from apps.access.models import Permission


from apps.access.models import Permission


class AuthorizationService:

    @staticmethod
    def _load_permissions(user):
        """
        Loads effective permission codes once per request.
        """
        if not hasattr(user, "_cached_permission_codes"):

            if user.is_superuser:
                # Superuser gets all permissions explicitly
                user._cached_permission_codes = set(
                    Permission.objects.values_list("code", flat=True)
                )
            else:
                user._cached_permission_codes = set(
                    Permission.objects
                    .filter(
                        permission_policies__policy__policy_users__user=user
                    )
                    .values_list("code", flat=True)
                    .distinct()
                )

        return user._cached_permission_codes


    @staticmethod
    def has_permission(user, permission_code: str) -> bool:
        if not user.is_active:
            return False

        permissions = AuthorizationService._load_permissions(user)
        return permission_code in permissions


    @staticmethod
    def get_user_permission_codes(user) -> set[str]:
        if not user.is_active:
            return set()

        return AuthorizationService._load_permissions(user)


    @staticmethod
    def get_user_systems(user) -> list[dict]:
        permission_codes = AuthorizationService.get_user_permission_codes(user)

        systems = {
            code.split(".")[0]
            for code in permission_codes
        }

        return [
            {
                "code": system,
                "label": system.upper(),
            }
            for system in sorted(systems)
        ]
        

    @staticmethod
    def group_permissions_by_system(permission_codes: set[str]) -> dict:
        grouped: dict[str, list[str]] = {}

        for code in permission_codes:
            parts = code.split(".", 1)
            if len(parts) != 2:
                continue

            system, remainder = parts

            grouped.setdefault(system, []).append(remainder)

        return {
            system: sorted(perms)
            for system, perms in grouped.items()
        }






# class AuthorizationService:

#     @staticmethod
#     def _load_permissions(user):
#         if not hasattr(user, "_cached_permission_codes"):
#             user._cached_permission_codes = set(
#                 Permission.objects.filter(
#                     permission_policies__policy__policy_users__user=user
#                 ).values_list("code", flat=True)
#             )
#         return user._cached_permission_codes

#     @staticmethod
#     def has_permission(user, permission_code: str) -> bool:
#         if not user.is_active:
#             return False
#         if user.is_superuser:
#             return True

#         permissions = AuthorizationService._load_permissions(user)
#         return permission_code in permissions

#     @staticmethod
#     def get_user_permission_codes(user) -> set[str]:
#         if not user.is_active:
#             return set()
#         if user.is_superuser:
#             return {"*"}

#         return AuthorizationService._load_permissions(user)

#     @staticmethod
#     def get_user_systems(user) -> list[dict]:
#         permission_codes = AuthorizationService.get_user_permission_codes(user)

#         systems = {
#             code.split(".")[0]
#             for code in permission_codes
#             if code != "*"
#         }

#         return [
#             {
#                 "code": system,
#                 "label": system.upper()  # or map to proper label registry
#             }
#             for system in sorted(systems)
#         ]
