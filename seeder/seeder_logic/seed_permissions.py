from apps.access.models import Permission
from ..seeder_data import PERMISSIONS

# --------------------
# Permissions
# --------------------
def seed_permissions():
    for code, service, description in PERMISSIONS:
        Permission.objects.get_or_create(
            code=code,
            defaults={
                "service": service,
                "description": description,
            },
        )