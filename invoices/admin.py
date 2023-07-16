from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from users.forms import CustomUserCreationForm, CustomUserChangeForm
from users.models import CustomUser
from .models import Invoice, Client, InvoiceItem


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ["email", "username"]


class InvoiceItemsInline(admin.TabularInline):
    model = InvoiceItem


class InvoiceAdmin(admin.ModelAdmin):
    inlines = [
        InvoiceItemsInline,
    ]
    readonly_fields = ("invoice_total",)


admin.site.register(Invoice, InvoiceAdmin)
admin.site.register(Client)
admin.site.register(InvoiceItem)
