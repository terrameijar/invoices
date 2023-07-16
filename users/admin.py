from django.contrib import admin
from django.contrib.auth.admin import UserAdmin


from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ["first_name", "last_name", "username", "email", "country"]

    fieldsets = (
        (
            "Personal Info",
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "username",
                    "password",
                    "phone_number",
                )
            },
        ),
        (
            "Company Info",
            {
                "classes": ("collapse",),
                "fields": (
                    "company",
                    "company_logo",
                    "address1",
                    "address2",
                    "country",
                ),
            },
        ),
        (
            "Permissions",
            {
                "classes": ("collapse",),
                "fields": ("is_active", "is_staff", "is_superuser"),
            },
        ),
    )


admin.site.register(CustomUser, CustomUserAdmin)
