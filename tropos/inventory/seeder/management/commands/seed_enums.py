from django.core.management.base import BaseCommand
from ...seed_logic import enums

class Command(BaseCommand):
    help = "Seed, unseed, or refresh the enums data."

    def add_arguments(self, parser):
        parser.add_argument(
            "--clear",
            action="store_true",
            help="Remove seeded enums data only."
        )
        parser.add_argument(
            "--fresh",
            action="store_true",
            help="Clear all enums data and reseed from scratch."
        )

    def handle(self, *args, **options):
        if options["fresh"]:
            self.stdout.write(self.style.WARNING("⚠️ Refreshing enums (clear + seed)..."))
            self.unseed_enums()
            self.seed_enums()
        elif options["clear"]:
            self.unseed_enums()
        else:
            self.seed_enums()

    def seed_enums(self):
        self.stdout.write(self.style.NOTICE("Seeding enums..."))
        enums.run()
        self.stdout.write(self.style.SUCCESS("✅ Enums seeding complete!"))

    def unseed_enums(self):
        self.stdout.write(self.style.WARNING("🗑️ Removing seeded enums..."))
        enums.revert()
        self.stdout.write(self.style.SUCCESS("🧹 enums data cleared."))
