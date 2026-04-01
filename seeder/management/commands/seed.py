from django.core.management.base import BaseCommand

# from ...seeder_logic import seed_department,seed_logic,seed_permission,seed_role,seed_rbac

# from ...seeder_logic.seed_departments import seed_departments
# from ...seeder_logic.seed_permissions import seed_permissions
# from ...seeder_logic.seed_roles import seed_roles, seed_role_permissions
# from ...seeder_logic.seed_department_allowed_roles import seed_department_allowed_roles
# from ...seeder_logic.seed_user import seed_super_admin
# from ...seeder_logic.rbac import seed_rbac

from inventory.seeder.seeder_logic import (
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

    def add_arguments(self, parser):
        parser.add_argument(
            "--fresh",
            action="store_true",
            help="Wipe all data before seeding (permissions, policies, roles, departments)",
        )

    def handle(self, *args, **options):
        if options["fresh"]:
            self.stdout.write(self.style.WARNING("🗑️  --fresh: wiping existing RBAC data..."))
            from apps.access.models import RolePolicy, PolicyPermission, Policy, Permission, Role, DepartmentAllowedSystem, UserRole
            from apps.department.models import Department
            from apps.identity.models import User

            UserRole.objects.all().delete()
            User.objects.all().delete()
            DepartmentAllowedSystem.objects.all().delete()
            Department.objects.all().delete()
            RolePolicy.objects.all().delete()
            PolicyPermission.objects.all().delete()
            Role.objects.all().delete()
            Policy.objects.all().delete()
            Permission.objects.all().delete()

            self.stdout.write(self.style.WARNING("✅ Wipe complete."))

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
