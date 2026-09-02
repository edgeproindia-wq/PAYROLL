from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from payroll_app.models import (
    Employee, SalaryStructure, Attendance, LeaveRequest, Reimbursement,
    PayrollRun, PayrollRunLine, ArrearsRecord, FullFinalSettlement,
    InvestmentDeclaration, OnboardingChecklist, SalaryTemplate, SalaryComponent,
    EmployeeSalaryComponent, UserRoleAssignment, EmailOTPVerification,
    EmailVerificationToken, UserRegistrationStatus, DemoRequest,
    Client, ClientProfile, ClientComplaint, CompanySettings
)

class Command(BaseCommand):
    def handle(self, *args, **options):
        keep_usernames = ["edgepro_admin"]

        models_to_wipe = [
            PayrollRunLine, PayrollRun, ArrearsRecord, FullFinalSettlement,
            InvestmentDeclaration, OnboardingChecklist, EmployeeSalaryComponent,
            SalaryComponent, SalaryTemplate, SalaryStructure, Attendance,
            LeaveRequest, Reimbursement, UserRoleAssignment,
            EmailOTPVerification, EmailVerificationToken, UserRegistrationStatus,
            DemoRequest, ClientComplaint, ClientProfile, Employee,
            Client, CompanySettings,
        ]

        for model in models_to_wipe:
            count = model.objects.count()
            model.objects.all().delete()
            self.stdout.write(f"Deleted {count} rows from {model.__name__}")

        deleted_users = User.objects.exclude(username__in=keep_usernames).delete()
        self.stdout.write(f"Deleted users (excluding {keep_usernames}): {deleted_users}")

        self.stdout.write(self.style.SUCCESS("Wipe complete. Only admin login(s) preserved."))
