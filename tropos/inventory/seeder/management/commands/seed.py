from django.core.management.base import BaseCommand
from django.core.management import call_command

class Command(BaseCommand):
  help = "Run all the seeders together"

  def add_arguments(self, parser):
    parser.add_argument(
      '--fresh', action='store_true',
      help='Flush database before seeding'
    )

  def handle(self, *args, **options):
    seeders = [
        "seed_accounts",
        "seed_enums",
        "seed_infrastructure",
        "seed_assets",
        
    ]

    if options["fresh"]:
      self.stdout.write(self.style.WARNING("Flushing database..."))
      call_command("flush", interactive=False)

    for seeder in seeders:
      self.stdout.write(self.style.NOTICE(f"Running {seeder}..."))
      call_command(seeder)

    self.stdout.write(self.style.SUCCESS("All seeders completed."))
