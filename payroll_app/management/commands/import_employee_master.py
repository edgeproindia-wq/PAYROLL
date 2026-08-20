import openpyxl
from django.core.management.base import BaseCommand
from payroll_app.models import Employee

STATUS_MAP = {
    "working": "ACTIVE",
    "terminated": "TERMINATED",
    "abscond": "TERMINATED",
}

class Command(BaseCommand):
    help = "Import employees from the Employees Master xlsx"

    def add_arguments(self, parser):
        parser.add_argument("filepath")
        parser.add_argument("--dry-run", action="store_true")

    def handle(self, *args, **opts):
        wb = openpyxl.load_workbook(opts["filepath"], data_only=True)
        ws = wb["Sheet1"]
        rows = list(ws.iter_rows(min_row=2, values_only=True))

        created, updated, skipped = 0, 0, 0

        for row in rows:
            code, name, manager, location, dept, team, designation, doj, status, lwd, remarks = row
            if not code or not name:
                skipped += 1
                continue

            name_parts = str(name).strip().split(" ", 1)
            first_name = name_parts[0]
            last_name = name_parts[1] if len(name_parts) > 1 else ""

            department = dept or team or "General"
            emp_status = STATUS_MAP.get(str(status).strip().lower(), "ACTIVE") if status else "ACTIVE"
            placeholder_email = f"{str(code).lower()}@edgepro.local"

            defaults = {
                "first_name": first_name,
                "last_name": last_name,
                "department": str(department),
                "designation": str(designation or "Not Specified"),
                "employment_status": emp_status,
                "date_of_joining": doj.date() if doj else "2025-01-01",
                "email": placeholder_email,
            }

            if opts["dry_run"]:
                self.stdout.write(f"Would upsert: {code} - {name} - {department} - {emp_status}")
                continue

            obj, was_created = Employee.objects.update_or_create(
                employee_code=str(code).strip(),
                defaults=defaults,
            )
            created += 1 if was_created else 0
            updated += 0 if was_created else 1

        self.stdout.write(self.style.SUCCESS(f"Done. Created={created} Updated={updated} Skipped={skipped}"))
