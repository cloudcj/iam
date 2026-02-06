# folder structure

    iam/
    ├── manage.py
    ├── iam/
    │   ├── seeds/
    │   │   └── bootstrap.py
    │   └── management/
    │       └── commands/
    │           └── seed.py
    ├── authz/
    │   └── seeds/
    │       └── rbac.py

    management/commands/seed.py

## in iam/management/commands/seed.py

    from django.core.management.base import BaseCommand

    from authz.seeds.rbac import seed_rbac
    from iam.seeds.bootstrap import seed_iam


    class Command(BaseCommand):
        help = "Seed IAM data (RBAC + bootstrap iam)"

        def handle(self, *args, **options):
            self.stdout.write("🌱 Seeding IAM data...")

            self.stdout.write("🔐 Seeding RBAC...")
            seed_rbac()

            self.stdout.write("👤 Seeding iam...")
            seed_iam()

            self.stdout.write(self.style.SUCCESS("✅ IAM seeding complete"))

## how you use it

    python manage.py seed
