from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),

    path('employee_master/', views.employee_master, name='employee_master'),
    path('employee_master/export/csv/', views.employee_master_export_csv, name='employee_master_export_csv'),
    path('employee/<int:pk>/edit/', views.employee_edit, name='employee_edit'),
    path('employee/<int:pk>/delete/', views.employee_delete, name='employee_delete'),

    path('salary_structure/', views.salary_structure, name='salary_structure'),
    path('attendance/', views.attendance, name='attendance'),
    path('leave_management/', views.leave_management, name='leave_management'),
    path('reimbursement/', views.reimbursement, name='reimbursement'),

    path('payslips/', views.payslips, name='payslips'),
    path('payslips/export/csv/', views.payslips_export_csv, name='payslips_export_csv'),
    path('payslips/export/excel/', views.payslips_export_excel, name='payslips_export_excel'),

    path('statutory_compliance/', views.statutory_compliance, name='statutory_compliance'),
    path('investment_declaration/', views.investment_declaration, name='investment_declaration'),
    path('income_tax/', views.income_tax, name='income_tax'),
    path('compliance_reports/', views.compliance_reports, name='compliance_reports'),

    path('total_employees/', views.total_employees_report, name='total_employees_report'),
    path('new_joiners/', views.new_joiners_report, name='new_joiners_report'),
    path('payroll_cost/', views.payroll_cost_report, name='payroll_cost_report'),
    path('pending_payroll/', views.pending_payroll_report, name='pending_payroll_report'),
    path('employees_on_leave/', views.employees_on_leave_report, name='employees_on_leave_report'),

    path('payroll_run/<int:pk>/', views.payroll_run_detail, name='payroll_run_detail'),
    path('payroll_run/<int:pk>/download/docx/', views.payroll_run_download_docx, name='payroll_run_download_docx'),
    path('payroll_run/<int:pk>/download/excel/', views.payroll_run_download_excel, name='payroll_run_download_excel'),
    path('payroll/', views.payroll_combined, name='payroll_combined'),
    path('payroll_processing/', views.payroll_combined, name='payroll_processing'),
    path('payroll_preview/', views.payroll_combined, name='payroll_preview'),
    path('payroll_validation/', views.payroll_combined, name='payroll_validation'),
    path('payroll_approval/', views.payroll_combined, name='payroll_approval'),
    path('payroll_release/', views.payroll_combined, name='payroll_release'),

    path('arrears/', views.arrears, name='arrears'),
    path('full_final_settlement/', views.full_final_settlement, name='full_final_settlement'),

    path('bank_transfer/', views.bank_transfer, name='bank_transfer'),
    path('bank_transfer/download_pdf/', views.download_pdf, name='download_pdf'),
    path('bank_transfer/failed_transaction_report/', views.failed_transaction_report, name='failed_transaction_report'),
    path('bank_transfer/payment_states/', views.payment_states, name='payment_states'),
    path('bank_transfer/salary_transfer_file/', views.salary_transfer_file, name='salary_transfer_file'),

    path('reports_analytics/', views.reports_analytics, name='reports_analytics'),
    path('ess/', views.ess, name='ess'),
    path('notifications/', views.notifications, name='notifications'),
    path('user_roles_permissions/', views.user_roles_permissions, name='user_roles_permissions'),
    path('settings/', views.settings, name='settings'),

    path('payslip_history/', views.payslip_history, name='payslip_history'),
    path('email_payslip/', views.email_payslip, name='email_payslip'),
    path('generate_payslip/', views.generate_payslip, name='generate_payslip'),

    path('page/<path:template_path>/', views.generic_page, name='generic_page'),
]

