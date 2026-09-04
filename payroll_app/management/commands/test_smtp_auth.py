from django.core.management.base import BaseCommand
from django.conf import settings
import smtplib

class Command(BaseCommand):
    def handle(self, *args, **options):
        host = settings.EMAIL_HOST
        port = settings.EMAIL_PORT
        user = settings.EMAIL_HOST_USER
        password = settings.EMAIL_HOST_PASSWORD

        self.stdout.write(f"Testing: host={host} port={port} user={user} password_length={len(password) if password else 0}")

        try:
            server = smtplib.SMTP(host, port, timeout=10)
            server.set_debuglevel(0)
            server.ehlo()
            server.starttls()
            server.ehlo()
            self.stdout.write(self.style.SUCCESS("TLS handshake OK, attempting login..."))
            server.login(user, password)
            self.stdout.write(self.style.SUCCESS("LOGIN SUCCESS"))
            server.quit()
        except smtplib.SMTPAuthenticationError as e:
            self.stdout.write(self.style.ERROR(f"AUTH FAILED: code={e.smtp_code} message={e.smtp_error}"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"OTHER ERROR: {type(e).__name__}: {e}"))
