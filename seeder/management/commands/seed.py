from django.core.management.base import BaseCommand

# from ...seeder_logic import seed_department,seed_logic,seed_permission,seed_role,seed_rbac

from ...seeder_logic.seed_departments import seed_departments
from ...seeder_logic.seed_permissions import seed_permissions
from ...seeder_logic.seed_roles import seed_roles, seed_role_permissions
from ...seeder_logic.seed_department_allowed_roles import seed_department_allowed_roles
from ...seeder_logic.seed_user import seed_super_admin
# from ...seeder_logic.rbac import seed_rbac


class Command(BaseCommand):
    help = "Seed IAM data (RBAC + bootstrap accounts)"

    def handle(self, *args, **options):
        self.stdout.write("🌱 Seeding IAM data...")

        # self.stdout.write("🔐 Seeding RBAC...")
        # seed_rbac()

        # self.stdout.write("👤 Seeding accounts...")
        # seed_accounts()

        self.stdout.write("🔐 Seeding...")
        seed_permissions()
        seed_roles()
        seed_role_permissions()
        seed_departments()
        seed_department_allowed_roles()
        seed_super_admin()

        self.stdout.write(self.style.SUCCESS("✅ IAM seeding complete"))
