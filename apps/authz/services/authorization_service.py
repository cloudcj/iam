# # iam/services/authorization.py

# from apps.access.models import Permission


# from apps.access.models import Permission


# class AuthorizationService:

#     @staticmethod
#     def _load_permissions(user):
#         """
#         Loads effective permission codes once per request.
#         """
#         if not hasattr(user, "_cached_permission_codes"):

#             if user.is_superuser:
#                 # Superuser gets all permissions explicitly
#                 user._cached_permission_codes = set(
#                     Permission.objects.values_list("code", flat=True)
#                 )
#             else:
#                 user._cached_permission_codes = set(
#                     Permission.objects
#                     .filter(
#                         permission_policies__policy__policy_users__user=user
#                     )
#                     .values_list("code", flat=True)
#                     .distinct()
#                 )

#         return user._cached_permission_codes


#     @staticmethod
#     def has_permission(user, permission_code: str) -> bool:
#         if not user.is_active:
#             return False

#         permissions = AuthorizationService._load_permissions(user)
#         return permission_code in permissions


#     @staticmethod
#     def get_user_permission_codes(user) -> set[str]:
#         if not user.is_active:
#             return set()

#         return AuthorizationService._load_permissions(user)


#     @staticmethod
#     def get_user_systems(user) -> list[dict]:
#         permission_codes = AuthorizationService.get_user_permission_codes(user)

#         systems = {
#             code.split(".")[0]
#             for code in permission_codes
#         }

#         return [
#             {
#                 "code": system,
#                 "label": system.upper(),
#             }
#             for system in sorted(systems)
#         ]
        

#     @staticmethod
#     def group_permissions_by_system(permission_codes: set[str]) -> dict:
#         grouped: dict[str, list[str]] = {}

#         for code in permission_codes:
#             parts = code.split(".", 1)
#             if len(parts) != 2:
#                 continue

#             system, remainder = parts

#             grouped.setdefault(system, []).append(remainder)

#         return {
#             system: sorted(perms)
#             for system, perms in grouped.items()
#         }

#######################################################

# from django.core.cache import cache
# from apps.access.models import Permission

# PERMISSION_CACHE_TTL = 30  # seconds
# PERMISSION_CACHE_PREFIX = "iam:permissions:"


# class AuthorizationService:

#     @staticmethod
#     def _cache_key(user_id) -> str:
#         return f"{PERMISSION_CACHE_PREFIX}{user_id}"

#     @staticmethod
#     def _load_permissions(user) -> set[str]:
#         """
#         Load effective permission codes.
#         1. Check per-request cache (user object attribute)
#         2. Check Redis TTL cache (30s)
#         3. Fall back to DB query
#         """

#         # Per-request cache (within same request lifecycle)
#         if hasattr(user, "_cached_permission_codes"):
#             return user._cached_permission_codes

#         # Redis TTL cache (across requests, 30s)
#         cache_key = AuthorizationService._cache_key(user.id)
#         cached = cache.get(cache_key)

#         if cached is not None:
#             user._cached_permission_codes = cached
#             return cached

#         # DB query
#         if user.is_superuser:
#             permissions = set(
#                 Permission.objects.values_list("code", flat=True)
#             )
#         else:
#             permissions = set(
#                 Permission.objects
#                 .filter(
#                     permission_policies__policy__policy_users__user=user
#                 )
#                 .values_list("code", flat=True)
#                 .distinct()
#             )

#         # Store in both caches
#         cache.set(cache_key, permissions, timeout=PERMISSION_CACHE_TTL)
#         user._cached_permission_codes = permissions

#         return permissions

#     @staticmethod
#     def invalidate_cache(user_id) -> None:
#         """
#         Call this when user permissions change.
#         Forces fresh DB load on next request.
#         """
#         cache.delete(f"{PERMISSION_CACHE_PREFIX}{user_id}")

#     @staticmethod
#     def has_permission(user, permission_code: str) -> bool:
#         if not user.is_active:
#             return False
#         permissions = AuthorizationService._load_permissions(user)
#         return permission_code in permissions

#     @staticmethod
#     def get_user_permission_codes(user) -> set[str]:
#         if not user.is_active:
#             return set()
#         return AuthorizationService._load_permissions(user)

#     @staticmethod
#     def get_user_systems(user) -> list[str]:
#         from registry.systems import PERMISSION_REGISTRY

#         permission_codes = AuthorizationService.get_user_permission_codes(user)
#         system_codes = {code.split(".")[0] for code in permission_codes}

#         return [
#             {
#                 "code": code,
#                 "label": PERMISSION_REGISTRY[code].label if code in PERMISSION_REGISTRY else code.capitalize(),
#             }
#             for code in sorted(system_codes)
#         ]

#     @staticmethod
#     def group_permissions_by_system(permission_codes: set[str]) -> dict:
#         """
#         Groups permission codes into system → resource → actions[].
#         e.g. "tropos.az.read" → { "tropos": { "az": ["read"] } }
#         """
#         grouped: dict[str, dict[str, list[str]]] = {}

#         for code in permission_codes:
#             parts = code.split(".")
#             if len(parts) != 3:
#                 continue

#             system, resource, action = parts
#             grouped.setdefault(system, {}).setdefault(resource, []).append(action)

#         return {
#             system: {
#                 resource: sorted(actions)
#                 for resource, actions in resources.items()
#             }
#             for system, resources in sorted(grouped.items())
#         }

######################################################################

from django.core.cache import cache
from apps.access.models import Permission

PERMISSION_CACHE_TTL = 30  # seconds
PERMISSION_CACHE_PREFIX = "iam:permissions:"


class AuthorizationService:

    @staticmethod
    def _cache_key(user_id) -> str:
        return f"{PERMISSION_CACHE_PREFIX}{user_id}"

    @staticmethod
    def _load_permissions(user) -> set[str]:
        """
        Load effective permission codes.
        1. Check per-request cache (user object attribute)
        2. Check Redis TTL cache (30s)
        3. Fall back to DB query — reads directly from UserPermission (source of truth)
        """

        # Per-request cache (within same request lifecycle)
        if hasattr(user, "_cached_permission_codes"):
            return user._cached_permission_codes

        # Redis TTL cache (across requests, 30s)
        cache_key = AuthorizationService._cache_key(user.id)
        cached = cache.get(cache_key)

        if cached is not None:
            user._cached_permission_codes = cached
            return cached

        # DB query — 1 hop: UserPermission → Permission
        if user.is_superuser:
            permissions = set(
                Permission.objects.values_list("code", flat=True)
            )
        else:
            permissions = set(
                Permission.objects
                .filter(iam_user_permissions__user=user)
                .values_list("code", flat=True)
                .distinct()
            )

        # Store in both caches
        cache.set(cache_key, permissions, timeout=PERMISSION_CACHE_TTL)
        user._cached_permission_codes = permissions

        return permissions

    @staticmethod
    def invalidate_cache(user_id) -> None:
        """
        Call this when user permissions change.
        Forces fresh DB load on next request.
        """
        cache.delete(f"{PERMISSION_CACHE_PREFIX}{user_id}")

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
    def get_user_systems(user) -> list[str]:
        from registry.systems import PERMISSION_REGISTRY

        permission_codes = AuthorizationService.get_user_permission_codes(user)
        system_codes = {code.split(".")[0] for code in permission_codes}

        return [
            {
                "code": code,
                "label": PERMISSION_REGISTRY[code].label if code in PERMISSION_REGISTRY else code.capitalize(),
            }
            for code in sorted(system_codes)
        ]

    @staticmethod
    def group_permissions_by_system(permission_codes: set[str]) -> dict:
        """
        Groups permission codes into system → resource → actions[].
        e.g. "tropos.az.read" → { "tropos": { "az": ["read"] } }
        """
        grouped: dict[str, dict[str, list[str]]] = {}

        for code in permission_codes:
            parts = code.split(".")
            if len(parts) != 3:
                continue

            system, resource, action = parts
            grouped.setdefault(system, {}).setdefault(resource, []).append(action)

        return {
            system: {
                resource: sorted(actions)
                for resource, actions in resources.items()
            }
            for system, resources in sorted(grouped.items())
        }