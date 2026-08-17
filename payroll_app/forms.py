from django import forms
from .models import Employee, SalaryStructure, Attendance, LeaveRequest, Reimbursement, PayrollRun, ArrearsRecord, FullFinalSettlement, UserRoleAssignment, CompanySettings, InvestmentDeclaration


class BootstrapFormMixin:
    """Adds Bootstrap 5 form-control/form-select classes to every field automatically."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            widget = field.widget
            if isinstance(widget, (forms.Select, forms.SelectMultiple)):
                existing = widget.attrs.get('class', '')
                widget.attrs['class'] = (existing + ' form-select').strip()
            elif isinstance(widget, forms.CheckboxInput):
                existing = widget.attrs.get('class', '')
                widget.attrs['class'] = (existing + ' form-check-input').strip()
            else:
                existing = widget.attrs.get('class', '')
                widget.attrs['class'] = (existing + ' form-control').strip()


class EmployeeForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = Employee
        exclude = ['employee_code']
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'date_of_joining': forms.DateInput(attrs={'type': 'date'}),
        }


class SalaryStructureForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = SalaryStructure
        fields = ['employee', 'basic', 'hra', 'conveyance', 'special_allowance']


class AttendanceForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = Attendance
        fields = ['employee', 'date', 'status', 'remarks']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }


class LeaveRequestForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = LeaveRequest
        fields = ['employee', 'leave_type', 'from_date', 'to_date', 'reason']
        widgets = {
            'from_date': forms.DateInput(attrs={'type': 'date'}),
            'to_date': forms.DateInput(attrs={'type': 'date'}),
        }


class ReimbursementForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = Reimbursement
        fields = ['employee', 'category', 'amount', 'date', 'description']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }


class PayrollRunForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = PayrollRun
        fields = ['month']


class ArrearsForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = ArrearsRecord
        fields = ['employee', 'effective_from', 'old_basic', 'new_basic', 'months']
        widgets = {'effective_from': forms.DateInput(attrs={'type': 'date'})}


class FullFinalSettlementForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = FullFinalSettlement
        fields = ['employee', 'last_working_day', 'pending_salary', 'leave_encashment', 'deductions']
        widgets = {'last_working_day': forms.DateInput(attrs={'type': 'date'})}


class UserRoleAssignmentForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = UserRoleAssignment
        fields = ['employee', 'role']


class CompanySettingsForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = CompanySettings
        fields = ['company_name', 'address', 'pan_number', 'gst_number', 'pf_percentage', 'esi_percentage', 'pf_wage_ceiling', 'casual_leave_days', 'sick_leave_days', 'earned_leave_days']


class InvestmentDeclarationForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = InvestmentDeclaration
        fields = ['employee', 'financial_year', 'section', 'investment_type', 'declared_amount']
