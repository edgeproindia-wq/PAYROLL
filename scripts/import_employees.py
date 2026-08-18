import openpyxl
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from payroll_app.models import Employee

STATUS_MAP = {
    'Working': 'ACTIVE',
    'In notice': 'ACTIVE',
    'Resigned': 'RESIGNED',
    'Terminated': 'TERMINATED',
    'Abscond': 'TERMINATED',
}

wb = openpyxl.load_workbook('Employees_Master_Data_updated_1__3_.xlsx', data_only=True)
ws = wb['Sheet1']

created = 0
skipped = 0

for row in ws.iter_rows(min_row=2, values_only=True):
    emp_code, name, manager, location, dept, team, designation, doj, status, lwd, remarks = row
    if not emp_code or not name:
        continue
    if Employee.objects.filter(employee_code=emp_code).exists():
        skipped += 1
        continue
    name_parts = name.strip().split(' ', 1)
    first_name = name_parts[0]
    last_name = name_parts[1] if len(name_parts) > 1 else ''
    status_clean = (status or '').strip()
    mapped_status = STATUS_MAP.get(status_clean, 'ACTIVE')
    Employee.objects.create(
        employee_code=emp_code,
        first_name=first_name,
        last_name=last_name,
        email=f'{emp_code.lower()}@company.com',
        department=dept or 'General',
        designation=designation or 'Staff',
        date_of_joining=doj.date() if doj else '2025-01-01',
        employment_status=mapped_status,
    )
    created += 1

print(f'Created: {created}, Skipped (already exist): {skipped}')
