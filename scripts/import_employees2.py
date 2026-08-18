import openpyxl
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from payroll_app.models import Employee

wb = openpyxl.load_workbook('Employees_Master_Data_Cleaned.xlsx', data_only=True)
ws = wb['Employees Master']

created = 0
skipped = 0

for row in ws.iter_rows(min_row=2, values_only=True):
    emp_id, name, reporting_to, branch, dept, sub_dept, designation, doj, status = row
    if not emp_id or not name:
        continue
    if Employee.objects.filter(employee_code=emp_id).exists():
        skipped += 1
        continue
    name_parts = name.strip().split(' ', 1)
    first_name = name_parts[0]
    last_name = name_parts[1] if len(name_parts) > 1 else ''
    Employee.objects.create(
        employee_code=emp_id,
        first_name=first_name,
        last_name=last_name,
        email=f'{emp_id.lower()}@company.com',
        department=dept or 'General',
        designation=designation or 'Staff',
        date_of_joining=doj.date() if doj else '2025-01-01',
        employment_status='ACTIVE',
    )
    created += 1

print(f'Created: {created}, Skipped (already exist): {skipped}')
