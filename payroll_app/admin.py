from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from .models import DemoRequest, EmailVerificationToken


@admin.action(description="Approve selected users (activate account)")
def approve_users(modeladmin, request, queryset):
    updated = queryset.update(is_active=True)
    modeladmin.message_user(request, f"{updated} user(s) approved and activated.")


@admin.action(description="Suspend selected users (deactivate account)")
def suspend_users(modeladmin, request, queryset):
    updated = queryset.update(is_active=False)
    modeladmin.message_user(request, f"{updated} user(s) suspended.")


class CustomUserAdmin(UserAdmin):
    list_display = ("username", "email", "is_active", "is_staff", "date_joined")
    list_filter = ("is_active", "is_staff", "date_joined")
    actions = [approve_users, suspend_users]


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)


@admin.register(DemoRequest)
class DemoRequestAdmin(admin.ModelAdmin):
    list_display = ("full_name", "company_name", "email", "phone", "created_at")
    search_fields = ("full_name", "company_name", "email", "phone")
    list_filter = ("created_at",)
    readonly_fields = ("created_at",)


@admin.register(EmailVerificationToken)
class EmailVerificationTokenAdmin(admin.ModelAdmin):
    list_display = ("user", "is_used", "email_verified", "created_at")
    list_filter = ("is_used", "email_verified")
    readonly_fields = ("token", "created_at")
