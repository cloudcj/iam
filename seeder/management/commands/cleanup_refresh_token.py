from django.core.management.base import BaseCommand
from django.utils.timezone import now
from datetime import timedelta

from identity.models import RefreshToken


class Command(BaseCommand):
    help = "Delete expired refresh tokens"

    def handle(self, *args, **options):
        cutoff = now() - timedelta(days=2)

        deleted_count, _ = RefreshToken.objects.filter(
            expires_at__lt=cutoff
        ).delete()

        self.stdout.write(
            self.style.SUCCESS(
                f"🧹 Deleted {deleted_count} expired refresh tokens"
            )
        )
