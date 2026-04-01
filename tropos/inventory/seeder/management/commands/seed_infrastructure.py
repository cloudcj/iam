from django.core.management.base import BaseCommand
from ...seed_logic import infrastructure

class Command(BaseCommand):
    help = "Seed, unseed, or refresh the infrastructure data."

    def add_arguments(self, parser):
        parser.add_argument(
            "--clear",
            action="store_true",
            help="Remove seeded infrastructure data only."
        )
        parser.add_argument(
            "--fresh",
            action="store_true",
            help="Clear all infrastructure data and reseed from scratch."
        )

    def handle(self, *args, **options):
        if options["fresh"]:
            self.stdout.write(self.style.WARNING("⚠️ Refreshing infrastructure (clear + seed)..."))
            self.unseed_infrastructure()
            self.seed_infrastructure()
        elif options["clear"]:
            self.unseed_infrastructure()
        else:
            self.seed_infrastructure()

    def seed_infrastructure(self):
        self.stdout.write(self.style.NOTICE("Seeding infrastructure..."))
        infrastructure.run()
        self.stdout.write(self.style.SUCCESS("✅ Infrastructure seeding complete!"))

    def unseed_infrastructure(self):
        self.stdout.write(self.style.WARNING("🗑️ Removing seeded infrastructure..."))
        infrastructure.revert()
        self.stdout.write(self.style.SUCCESS("🧹 Infrastructure data cleared."))

   