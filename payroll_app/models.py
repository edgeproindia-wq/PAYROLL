from django.db import models
from django.contrib.auth.models import User


class Employee(models.Model):
    EMPLOYMENT_STATUS_CHOICES = [
        ('ACTIVE', 'Active'),
        ('ON_LEAVE', 'On Leave'),
        ('RESIGNED', 'Resigned'),
        ('TERMINATED', 'Terminated'),
    ]
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]

    employee_code = models.CharField(max_length=20, unique=True, help_text='e.g. EMP0001')
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='employee_profile')
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100, blank=True)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_joining = models.DateField()
    department = models.CharField(max_length=200)
    designation = models.CharField(max_length=200)
    employment_status = models.CharField(max_length=20, choices=EMPLOYMENT_STATUS_CHOICES, default='ACTIVE')
    pan_number = models.CharField(max_length=10, blank=True)
    aadhar_number = models.CharField(max_length=12, blank=True)
    bank_account_no = models.CharField(max_length=30, blank=True)
    ifsc_code = models.CharField(max_length=11, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['employee_code']

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}".strip()

    def __str__(self):
        return f"{self.employee_code} - {self.full_name}"


class SalaryStructure(models.Model):
    employee = models.OneToOneField(Employee, on_delete=models.CASCADE, related_name='salary_structure')
    basic = models.DecimalField(max_digits=10, decimal_places=2)
    hra = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    conveyance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    special_allowance = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    @property
    def gross_salary(self):
        return self.basic + self.hra + self.conveyance + self.special_allowance

    def __str__(self):
        return f"Salary structure for {self.employee}"


class Attendance(models.Model):
    STATUS_CHOICES = [
        ('PRESENT', 'Present'),
        ('ABSENT', 'Absent'),
        ('HALF_DAY', 'Half Day'),
        ('LEAVE', 'On Leave'),
    ]

    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='attendance_records')
    date = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PRESENT')
    remarks = models.CharField(max_length=255, blank=True)

    class Meta:
        ordering = ['-date']
        unique_together = ('employee', 'date')

    def __str__(self):
        return f"{self.employee} - {self.date} - {self.status}"


class LeaveRequest(models.Model):
    LEAVE_TYPE_CHOICES = [
        ('CASUAL', 'Casual Leave'),
        ('SICK', 'Sick Leave'),
        ('EARNED', 'Earned Leave'),
    ]
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
    ]

    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='leave_requests')
    leave_type = models.CharField(max_length=10, choices=LEAVE_TYPE_CHOICES)
    from_date = models.DateField()
    to_date = models.DateField()
    reason = models.CharField(max_length=255, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')

    class Meta:
        ordering = ['-from_date']

    def __str__(self):
        return f"{self.employee} - {self.leave_type} - {self.status}"


class Reimbursement(models.Model):
    CATEGORY_CHOICES = [
        ('TRAVEL', 'Travel'),
        ('MEDICAL', 'Medical'),
        ('FOOD', 'Food'),
        ('OTHER', 'Other'),
    ]
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
    ]

    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='reimbursements')
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    description = models.CharField(max_length=255, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return f"{self.employee} - {self.category} - {self.amount}"


class PayrollRun(models.Model):
    STATUS_CHOICES = [
        ('DRAFT', 'Draft'),
        ('VALIDATED', 'Validated'),
        ('APPROVED', 'Approved'),
        ('RELEASED', 'Released'),
    ]

    month = models.CharField(max_length=20, help_text='e.g. August 2026')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='DRAFT')
    is_locked = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.month} ({self.status})"


class PayrollRunLine(models.Model):
    payroll_run = models.ForeignKey(PayrollRun, on_delete=models.CASCADE, related_name='lines')
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    basic = models.DecimalField(max_digits=10, decimal_places=2)
    gross_salary = models.DecimalField(max_digits=10, decimal_places=2)
    net_pay = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.payroll_run} - {self.employee}"


class CompanySettings(models.Model):
    company_name = models.CharField(max_length=200, default='My Company')
    address = models.CharField(max_length=500, blank=True)
    pan_number = models.CharField(max_length=10, blank=True)
    gst_number = models.CharField(max_length=15, blank=True)
    pf_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=12.0)
    esi_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0.75)
    pf_wage_ceiling = models.DecimalField(max_digits=10, decimal_places=2, default=21000.0)
    casual_leave_days = models.IntegerField(default=12)
    sick_leave_days = models.IntegerField(default=12)
    earned_leave_days = models.IntegerField(default=15)

    def __str__(self):
        return self.company_name


class ArrearsRecord(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='arrears_records')
    effective_from = models.DateField()
    old_basic = models.DecimalField(max_digits=10, decimal_places=2)
    new_basic = models.DecimalField(max_digits=10, decimal_places=2)
    months = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Arrears - {self.employee} - {self.effective_from}"


class FullFinalSettlement(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='settlements')
    last_working_day = models.DateField()
    pending_salary = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    leave_encashment = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    deductions = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"F&F - {self.employee}"


class UserRoleAssignment(models.Model):
    ROLE_CHOICES = [
        ('ADMIN', 'Admin'),
        ('HR', 'HR'),
        ('FINANCE', 'Finance'),
        ('PAYROLL_EXECUTIVE', 'Payroll Executive'),
        ('REPORTING_MANAGER', 'Reporting Manager'),
        ('EMPLOYEE', 'Employee'),
    ]

    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='role_assignments')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    assigned_on = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.employee} - {self.role}"


class InvestmentDeclaration(models.Model):
    SECTION_CHOICES = [
        ('80C', 'Section 80C'),
        ('80D', 'Section 80D'),
        ('80CCD', 'Section 80CCD (NPS)'),
        ('HRA', 'HRA Exemption'),
        ('OTHER', 'Other'),
    ]

    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='investment_declarations')
    financial_year = models.CharField(max_length=9, help_text='e.g. 2026-2027')
    section = models.CharField(max_length=10, choices=SECTION_CHOICES)
    investment_type = models.CharField(max_length=100)
    declared_amount = models.DecimalField(max_digits=10, decimal_places=2)
    proof_document = models.CharField(max_length=255, blank=True)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.employee} - {self.financial_year} - {self.section}"
