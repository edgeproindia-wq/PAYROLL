from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

class Command(BaseCommand):
    def handle(self, *args, **options):
        user, created = User.objects.get_or_create(username="admin", defaults={"is_staff": True, "is_superuser": True})
        user.is_staff = True
        user.is_superuser = True
        user.set_password("EdgePro@2026")
        user.save()
        self.stdout.write("Admin password reset successfully.")
