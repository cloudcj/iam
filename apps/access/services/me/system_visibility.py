from apps.access.models import Permission


def get_visible_systems_for_user(user):
    """
    Returns a sorted list of unique system codes
    derived from user's effective permissions.
    """

    if user.is_superuser:
        # Superuser sees all systems
        permission_codes = Permission.objects.values_list("code", flat=True)
    else:
        permission_codes = (
            Permission.objects
            .filter(
                permission_policies__policy__policy_users__user=user
            )
            .values_list("code", flat=True)
            .distinct()
        )

    systems = {
        code.split(".")[0]
        for code in permission_codes
    }

    return sorted(systems)
