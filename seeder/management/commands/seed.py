from django.core.management.base import BaseCommand

# from ...seeder_logic import seed_department,seed_logic,seed_permission,seed_role,seed_rbac

# from ...seeder_logic.seed_departments import seed_departments
# from ...seeder_logic.seed_permissions import seed_permissions
# from ...seeder_logic.seed_roles import seed_roles, seed_role_permissions
# from ...seeder_logic.seed_department_allowed_roles import seed_department_allowed_roles
# from ...seeder_logic.seed_user import seed_super_admin
# from ...seeder_logic.rbac import seed_rbac

from seeder.seeder_logic import (
    seed_permissions,
    seed_policies,
    seed_policy_permissions,
    seed_roles,
    seed_role_policies,
    # seed_role_permissions,
    seed_departments,
    seed_department_allowed_systems,
    seed_superadmin

)
class Command(BaseCommand):
    help = "Seed IAM data (RBAC + bootstrap accounts)"

    def handle(self, *args, **options):
        self.stdout.write("🌱 Seeding IAM data...")

        self.stdout.write("🔐 Seeding permissions...")
        seed_permissions()

        self.stdout.write("📜 Seeding policies...")
        seed_policies()  # includes policy-permission mapping

        self.stdout.write("👥 Seeding roles...")
        seed_roles()
        # seed_role_policies()

        self.stdout.write("🏢 Seeding departments...")
        seed_departments()
        seed_department_allowed_systems()

        self.stdout.write("👑 Seeding superadmin...")
        seed_superadmin()

        self.stdout.write(self.style.SUCCESS("✅ IAM seeding complete"))

