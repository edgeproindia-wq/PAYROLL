from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('employee_master/', views.employee_master, name='employee_master'),
    path('salary_structure/', views.salary_structure, name='salary_structure'),
    path('attendance/', views.attendance, name='attendance'),
    path('leave_management/', views.leave_management, name='leave_management'),
    path('reimbursement/', views.reimbursement, name='reimbursement'),
    path('payroll_processing/', views.payroll_processing, name='payroll_processing'),
    path('payroll_preview/', views.payroll_preview, name='payroll_preview'),
    path('payroll_validation/', views.payroll_validation, name='payroll_validation'),
    path('payroll_approval/', views.payroll_approval, name='payroll_approval'),
    path('payroll_release/', views.payroll_release, name='payroll_release'),
    path('statutory_compliance/', views.statutory_compliance, name='statutory_compliance'),
    path('income_tax/', views.income_tax, name='income_tax'),
    path('compliance_reports/', views.compliance_reports, name='compliance_reports'),
    path('arrears/', views.arrears, name='arrears'),
    path('full_final_settlement/', views.full_final_settlement, name='full_final_settlement'),
    path('payslips/', views.payslips, name='payslips'),
    path('bank_transfer/', views.bank_transfer, name='bank_transfer'),
    path('reports_analytics/', views.reports_analytics, name='reports_analytics'),
    path('ess/', views.ess, name='ess'),
    path('notifications/', views.notifications, name='notifications'),
    path('user_roles_permissions/', views.user_roles_permissions, name='user_roles_permissions'),
    path('settings/', views.settings, name='settings'),
]
