from django import forms
from .models import Employee, SalaryStructure, Attendance, LeaveRequest, Reimbursement, PayrollRun, ArrearsRecord, FullFinalSettlement, UserRoleAssignment, CompanySettings, InvestmentDeclaration, OnboardingChecklist


class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = '__all__'
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'date_of_joining': forms.DateInput(attrs={'type': 'date'}),
        }


class SalaryStructureForm(forms.ModelForm):
    class Meta:
        model = SalaryStructure
        fields = ['employee', 'basic', 'hra', 'conveyance', 'special_allowance']


class AttendanceForm(forms.ModelForm):
    class Meta:
        model = Attendance
        fields = ['employee', 'date', 'status', 'remarks']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }


class LeaveRequestForm(forms.ModelForm):
    class Meta:
        model = LeaveRequest
        fields = ['employee', 'leave_type', 'from_date', 'to_date', 'reason']
        widgets = {
            'from_date': forms.DateInput(attrs={'type': 'date'}),
            'to_date': forms.DateInput(attrs={'type': 'date'}),
        }


class ReimbursementForm(forms.ModelForm):
    class Meta:
        model = Reimbursement
        fields = ['employee', 'category', 'amount', 'date', 'description']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }


class PayrollRunForm(forms.ModelForm):
    class Meta:
        model = PayrollRun
        fields = ['month']


class ArrearsForm(forms.ModelForm):
    class Meta:
        model = ArrearsRecord
        fields = ['employee', 'effective_from', 'old_basic', 'new_basic', 'months']
        widgets = {'effective_from': forms.DateInput(attrs={'type': 'date'})}


class FullFinalSettlementForm(forms.ModelForm):
    class Meta:
        model = FullFinalSettlement
        fields = ['employee', 'last_working_day', 'pending_salary', 'leave_encashment', 'deductions']
        widgets = {'last_working_day': forms.DateInput(attrs={'type': 'date'})}


class UserRoleAssignmentForm(forms.ModelForm):
    class Meta:
        model = UserRoleAssignment
        fields = ['employee', 'role']


class CompanySettingsForm(forms.ModelForm):
    class Meta:
        model = CompanySettings
        fields = ['company_name', 'address', 'pan_number', 'gst_number', 'pf_percentage', 'esi_percentage', 'pf_wage_ceiling', 'casual_leave_days', 'sick_leave_days', 'earned_leave_days']


class InvestmentDeclarationForm(forms.ModelForm):
    class Meta:
        model = InvestmentDeclaration
        fields = ['employee', 'financial_year', 'section', 'investment_type', 'declared_amount']

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]


class OnboardingChecklistForm(forms.ModelForm):
    class Meta:
        model = OnboardingChecklist
        fields = ["employee", "is_offboarding", "offer_letter_signed", "documents_collected", "bank_details_verified", "it_equipment_assigned", "orientation_scheduled", "exit_interview_done", "assets_returned"]

