from django.core.management.base import BaseCommand
from ...seed_logic import accounts

class Command(BaseCommand):
    help = "Seed, unseed, or refresh the accounts data."

    def add_arguments(self, parser):
        parser.add_argument(
            "--clear",
            action="store_true",
            help="Remove seeded accounts data only."
        )
        parser.add_argument(
            "--fresh",
            action="store_true",
            help="Clear all accounts data and reseed from scratch."
        )

    def handle(self, *args, **options):
        if options["fresh"]:
            self.stdout.write(self.style.WARNING("⚠️ Refreshing accounts (clear + seed)..."))
            self.unseed_accounts()
            self.seed_accounts()
        elif options["clear"]:
            self.unseed_accounts()
        else:
            self.seed_accounts()

    def seed_accounts(self):
        self.stdout.write(self.style.NOTICE("Seeding accounts..."))
        accounts.run()
        self.stdout.write(self.style.SUCCESS("✅ Accounts seeding complete!"))

    def unseed_accounts(self):
        self.stdout.write(self.style.WARNING("🗑️ Removing seeded accounts..."))
        accounts.revert()
        self.stdout.write(self.style.SUCCESS("🧹 Accounts data cleared."))

   