from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):

    # Fields that show in list view
    list_display = (
        "username", "email", "first_name", "last_name",
        "phone", "location", "occupation", "is_staff"
    )
    list_filter = (
        "is_staff", "is_superuser", "is_active",
        "location", "occupation"
    )

    # Fields in detail (edit) view
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (_("Personal info"), {
            "fields": (
                "first_name", "last_name", "email",
                "phone", "profile_picture",
                "facebook_account", "location", "occupation"
            )
        }),
        (_("Permissions"), {
            "fields": (
                "is_active", "is_staff", "is_superuser",
                "groups", "user_permissions"
            )
        }),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )

    # Fields used when creating a user in admin
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": (
                "username", "email",
                "password1", "password2"
            ),
        }),
    )

    search_fields = ("username", "email", "first_name", "last_name")
    ordering = ("id",)
