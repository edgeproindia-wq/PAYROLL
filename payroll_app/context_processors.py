def notification_count(request):
    if not request.user.is_authenticated:
        return {}
    from .models import LeaveRequest, Reimbursement, PayrollRun, UserRegistrationStatus
    count = (
        LeaveRequest.objects.filter(status='PENDING').count()
        + Reimbursement.objects.filter(status='PENDING').count()
        + PayrollRun.objects.filter(status='VALIDATED').count()
        + UserRegistrationStatus.objects.filter(status='PENDING').count()
    )
    return {'notification_count': count}
