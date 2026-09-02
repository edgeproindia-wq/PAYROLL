from django.db import models


class EmployeeManager(models.Manager):
    def numeric_order(self):
        def sort_key(emp):
            digits = ''.join(filter(str.isdigit, emp.employee_code))
            return int(digits) if digits else 0
        return sorted(self.get_queryset(), key=sort_key)


class Client(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('ACTIVE', 'Active'),
        ('INACTIVE', 'Inactive'),
        ('SUSPENDED', 'Suspended'),
        ('REJECTED', 'Rejected'),
    ]
    company_name = models.CharField(max_length=200)
    contact_name = models.CharField(max_length=150, blank=True)
    email = models.EmailField(unique=True)
    mobile = models.CharField(max_length=15, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')
    rejection_reason = models.TextField(blank=True)
    approved_by = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True, blank=True, related_name='approved_clients')
    approved_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.company_name


class ClientProfile(models.Model):
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE, related_name='client_profile')
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='profiles')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.client.company_name}"


class ClientComplaint(models.Model):
    STATUS_CHOICES = [
        ('OPEN', 'Open'),
        ('IN_PROGRESS', 'In Progress'),
        ('RESOLVED', 'Resolved'),
        ('CLOSED', 'Closed'),
    ]
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='complaints')
    raised_by = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True, blank=True, related_name='raised_complaints')
    subject = models.CharField(max_length=200)
    description = models.TextField()
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='OPEN')
    admin_response = models.TextField(blank=True)
    resolved_by = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True, blank=True, related_name='resolved_complaints')
    resolved_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.subject + " - " + self.client.company_name


class Employee(models.Model):
    user = models.OneToOneField('auth.User', on_delete=models.SET_NULL, null=True, blank=True, related_name='employee_profile')
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='employees', null=True, blank=True)
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
    bank_name = models.CharField(max_length=100, blank=True)
    account_holder_name = models.CharField(max_length=150, blank=True)
    branch_name = models.CharField(max_length=150, blank=True)
    ACCOUNT_TYPE_CHOICES = [('SAVINGS', 'Savings'), ('CURRENT', 'Current')]
    account_type = models.CharField(max_length=10, choices=ACCOUNT_TYPE_CHOICES, blank=True)
    upi_id = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['employee_code']

    objects = EmployeeManager()

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}".strip()

    @property
    def total_earnings_from_components(self):
        components = self.salary_components.filter(is_active=True, component__component_type="EARNING")
        return sum(c.computed_amount for c in components)

    @property
    def total_deductions_from_components(self):
        components = self.salary_components.filter(is_active=True, component__component_type="DEDUCTION")
        return sum(c.computed_amount for c in components)

    @property
    def net_from_components(self):
        return self.total_earnings_from_components - self.total_deductions_from_components

    @property
    def has_configurable_salary(self):
        return self.salary_components.filter(is_active=True).exists()

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
    approved_by = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True, blank=True, related_name='approved_leaves')
    approved_at = models.DateTimeField(null=True, blank=True)
    rejection_reason = models.TextField(blank=True)

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
    hra = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    special_allowance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    other_allowances = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    pf_deduction = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    esi_deduction = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    professional_tax = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    loan_deduction = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    insurance_premium = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    other_deductions = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.payroll_run} - {self.employee}"


class CompanySettings(models.Model):
    company_name = models.CharField(max_length=200, default='My Company')
    client = models.OneToOneField('payroll_app.Client', on_delete=models.CASCADE, related_name='settings', null=True, blank=True)
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

    @property
    def difference(self):
        return self.new_basic - self.old_basic

    @property
    def total_arrears(self):
        return self.difference * self.months

    def __str__(self):
        return f"Arrears - {self.employee} - {self.effective_from}"


class FullFinalSettlement(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='settlements')
    last_working_day = models.DateField()
    pending_salary = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    leave_encashment = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    deductions = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def net_settlement(self):
        return self.pending_salary + self.leave_encashment - self.deductions

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




class OnboardingChecklist(models.Model):
    employee = models.OneToOneField(Employee, on_delete=models.CASCADE, related_name="onboarding")
    offer_letter_signed = models.BooleanField(default=False)
    documents_collected = models.BooleanField(default=False)
    bank_details_verified = models.BooleanField(default=False)
    it_equipment_assigned = models.BooleanField(default=False)
    orientation_scheduled = models.BooleanField(default=False)
    is_offboarding = models.BooleanField(default=False, help_text="Check if this is an offboarding checklist instead of onboarding")
    exit_interview_done = models.BooleanField(default=False)
    assets_returned = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def completion_percent(self):
        if self.is_offboarding:
            fields = [self.exit_interview_done, self.assets_returned, self.documents_collected]
        else:
            fields = [self.offer_letter_signed, self.documents_collected, self.bank_details_verified, self.it_equipment_assigned, self.orientation_scheduled]
        done = sum(1 for f in fields if f)
        return int((done / len(fields)) * 100) if fields else 0

    def __str__(self):
        return f"{'Offboarding' if self.is_offboarding else 'Onboarding'} - {self.employee.full_name}"


class SalaryComponent(models.Model):
    COMPONENT_TYPE_CHOICES = [("EARNING", "Earning"), ("DEDUCTION", "Deduction")]
    CALC_TYPE_CHOICES = [("FIXED", "Fixed Amount"), ("PERCENTAGE", "Percentage of Basic")]

    name = models.CharField(max_length=100, unique=True)
    component_type = models.CharField(max_length=10, choices=COMPONENT_TYPE_CHOICES)
    calculation_type = models.CharField(max_length=12, choices=CALC_TYPE_CHOICES, default="FIXED")
    is_taxable = models.BooleanField(default=True)
    is_employer_contribution = models.BooleanField(default=False)
    include_in_ctc = models.BooleanField(default=True)
    show_in_payslip = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["component_type", "name"]

    def __str__(self):
        return f"{self.name} ({self.get_component_type_display()})"


class SalaryTemplate(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.CharField(max_length=255, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class SalaryTemplateComponent(models.Model):
    template = models.ForeignKey(SalaryTemplate, on_delete=models.CASCADE, related_name="components")
    component = models.ForeignKey(SalaryComponent, on_delete=models.CASCADE)
    value = models.DecimalField(max_digits=10, decimal_places=2, help_text="Fixed amount, or percentage if component is percentage-based")

    class Meta:
        unique_together = ("template", "component")

    def __str__(self):
        return f"{self.template.name} - {self.component.name}"


class EmployeeSalaryComponent(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name="salary_components")
    component = models.ForeignKey(SalaryComponent, on_delete=models.CASCADE)
    value = models.DecimalField(max_digits=10, decimal_places=2, help_text="Fixed amount, or percentage if component is percentage-based")
    effective_from = models.DateField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("employee", "component", "effective_from")
        ordering = ["-effective_from"]

    def __str__(self):
        return f"{self.employee.full_name} - {self.component.name}"

    @property
    def computed_amount(self):
        if self.component.calculation_type == "PERCENTAGE":
            basic = EmployeeSalaryComponent.objects.filter(
                employee=self.employee, component__name__iexact="Basic", is_active=True
            ).order_by("-effective_from").first()
            basic_value = basic.value if basic else 0
            return round(basic_value * self.value / 100, 2)
        return self.value



class DemoRequest(models.Model):
    STATUS_CHOICES = [
        ('NEW', 'New'),
        ('CONTACTED', 'Contacted'),
        ('CLOSED', 'Closed'),
    ]
    full_name = models.CharField(max_length=150)
    company_name = models.CharField(max_length=150)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    message = models.TextField(blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='NEW')
    handled_by = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True, blank=True, related_name='handled_demo_requests')
    handled_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.full_name} - {self.company_name}"


class EmailVerificationToken(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    token = models.CharField(max_length=64, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_used = models.BooleanField(default=False)
    email_verified = models.BooleanField(default=False)

    def __str__(self):
        return f"Token for {self.user.username}"



class EmailOTPVerification(models.Model):
    email = models.EmailField()
    otp_hash = models.CharField(max_length=128)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    last_sent_at = models.DateTimeField(auto_now_add=True)
    attempts = models.IntegerField(default=0)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return f"OTP for {self.email} (verified={self.is_verified})"


class UserRegistrationStatus(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('ACTIVE', 'Active'),
        ('REJECTED', 'Rejected'),
    ]
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE, related_name='registration_status')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')
    rejection_reason = models.TextField(blank=True)
    activated_by = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True, blank=True, related_name='activated_users')
    activated_at = models.DateTimeField(null=True, blank=True)
    rejected_by = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True, blank=True, related_name='rejected_users')
    rejected_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.status}"
