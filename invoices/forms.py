from django.forms import ModelForm
from .models import Invoice, InvoiceItem, Client


class InvoiceItemsForm(ModelForm):
    class Meta:
        model = InvoiceItem
        fields = "__all__"


class InvoiceCreateForm(ModelForm):
    class Meta:
        model = Invoice
        fields = ["title", "client"]

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user")
        super(InvoiceCreateForm, self).__init__(*args, **kwargs)
        self.fields["client"].queryset = Client.objects.filter(created_by=user)
