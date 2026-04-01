# myapp/management/commands/seed_all.py
from django.core.management.base import BaseCommand

# import your seeders
from ...seed_logic import interface, switch, server, appliance

class Command(BaseCommand):
    help = "Seed, unseed, or refresh the assets data."

    def add_arguments(self, parser):
        parser.add_argument(
            "--clear",
            action="store_true",
            help="Remove seeded assets data only."
        )
        parser.add_argument(
            "--fresh",
            action="store_true",
            help="Clear all assets data and reseed from scratch."
        )

    def handle(self, *args, **options):
        if options["fresh"]:
            self.stdout.write(self.style.WARNING("⚠️ Refreshing assets (clear + seed)..."))
            self.unseed_assets()
            self.seed_assets()
        elif options["clear"]:
            self.unseed_assets()
        else:
            self.seed_assets()

    def seed_assets(self):
        self.stdout.write(self.style.NOTICE("Seeding assets..."))
        appliance.run()
        switch.run()
        server.run()
        interface.run()
        self.stdout.write(self.style.SUCCESS("✅ Assets seeding complete!"))

    def unseed_assets(self):
        self.stdout.write(self.style.WARNING("🗑️ Removing seeded assets..."))
        switch.revert()
        server.revert()
        appliance.revert()
        interface.revert()
        # power_supply_units.revert()
        # fan_units.revert()
        self.stdout.write(self.style.SUCCESS("🧹 assets data cleared."))

   