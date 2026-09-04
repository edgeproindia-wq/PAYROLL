from django.core.management.base import BaseCommand
import socket

class Command(BaseCommand):
    def handle(self, *args, **options):
        targets = [
            ("smtp.gmail.com", 587),
            ("smtp.gmail.com", 465),
            ("smtp.gmail.com", 25),
        ]
        for host, port in targets:
            try:
                sock = socket.create_connection((host, port), timeout=8)
                self.stdout.write(self.style.SUCCESS(f"SUCCESS: Connected to {host}:{port}"))
                sock.close()
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"FAILED: {host}:{port} - {type(e).__name__}: {e}"))
