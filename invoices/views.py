from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.files.storage import FileSystemStorage
from django.forms.models import inlineformset_factory
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.template.loader import render_to_string
from django.urls import reverse, reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)
from weasyprint import HTML

from .forms import InvoiceCreateForm, InvoiceEditForm, ClientCreateForm
from .models import Client, Invoice, InvoiceItem

InvoiceItemsFormset = inlineformset_factory(
    Invoice,
    InvoiceItem,
    fields=(
        "item",
        "quantity",
        "rate",
    ),
    extra=1,
)


class HomePage(ListView):
    template_name = "home.html"
    context_object_name = "invoices"
    paginate_by = 10

    def get_queryset(self):
        if self.request.user.is_authenticated:
            invoices = Invoice.objects.filter(user=self.request.user).order_by(
                "-create_date"
            )
            return invoices
        else:
            return Invoice.objects.none()

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get the data
        context = super(HomePage, self).get_context_data(**kwargs)
        try:
            recent_invoices = context["invoices"][:4]
        except (IndexError, AttributeError):
            recent_invoices = None
        context["recent_invoices"] = recent_invoices
        return context


class InvoiceListView(LoginRequiredMixin, ListView):
    template_name = "dashboard.html"

    def get_queryset(self):
        if self.request.user.is_authenticated:
            invoices = Invoice.objects.filter(user=self.request.user)
            return invoices
        else:
            return Invoice.objects.none()


class InvoiceDetailView(LoginRequiredMixin, DetailView):
    template_name = "invoice_detail.html"

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Invoice.objects.filter(user=self.request.user)
        else:
            return Invoice.objects.none()

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get the data
        context = super(InvoiceDetailView, self).get_context_data(**kwargs)
        # Add client to the context -- to be used by invoice template
        client = context["invoice"].client
        context["client"] = client
        # Add invoice items queryset
        context["invoice_items"] = context["invoice"].items.all()
        user = context["invoice"].user
        context["user"] = user
        return context


class InvoiceCreateView(LoginRequiredMixin, CreateView):
    model = Invoice
    template_name = "new_invoice.html"
    form_class = InvoiceCreateForm

    def get_form_kwargs(self):
        # The queryset for this view was created in the form
        # get_queryset() isn't used in create views
        kwargs = super(InvoiceCreateView, self).get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def get_context_data(self, **kwargs):
        # To display the invoice items
        # Call the base implementation first to get the data
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data["invoice_items"] = InvoiceItemsFormset(self.request.POST)
        else:
            data["invoice_items"] = InvoiceItemsFormset()
        return data

    def form_valid(self, form):
        form.instance.user = self.request.user
        context = self.get_context_data()
        invoice_items = context["invoice_items"]
        self.invoice = form.save()
        if invoice_items.is_valid():
            invoice_items.instance = self.invoice
            invoice_items.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("invoice-detail", args=[self.object.pk])


class InvoiceUpdateView(LoginRequiredMixin, UpdateView):
    # fields = ["title", "client", "invoice_terms"]
    template_name = "edit_invoice.html"
    form_class = InvoiceEditForm

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Invoice.objects.filter(user=self.request.user)
        else:
            return Invoice.objects.none()

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data["invoice_items"] = InvoiceItemsFormset(
                self.request.POST, instance=self.object
            )
        else:
            data["invoice_items"] = InvoiceItemsFormset(instance=self.object)
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        invoice_items = context["invoice_items"]
        self.object = form.save()
        if invoice_items.is_valid():
            invoice_items.instance = self.object
            invoice_items.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("invoice-detail", args=[self.object.pk])


class InvoiceDeleteView(LoginRequiredMixin, DeleteView):
    template_name = "confirm_delete_invoice.html"
    success_url = reverse_lazy("invoice-list")

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Invoice.objects.filter(user=self.request.user)
        else:
            return Invoice.objects.none()


class ClientCreateView(LoginRequiredMixin, CreateView):
    model = Client
    template_name = "new_client.html"
    form_class = ClientCreateForm

    def form_valid(self, form):
        client = form.save(commit=False)
        client.created_by = self.request.user
        client.save()
        return super().form_valid(form)


class ClientListView(LoginRequiredMixin, ListView):
    template_name = "clients.html"

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Client.objects.filter(created_by=self.request.user)
        else:
            return Client.objects.none()


class ClientDetailView(LoginRequiredMixin, DetailView):
    template_name = "client_detail.html"

    def get_object(self):
        client = super().get_object()
        return client

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Client.objects.filter(created_by=self.request.user)
        else:
            return Client.objects.none()

    def get_invoices_set(self):
        if self.request.user.is_authenticated:
            return Invoice.objects.filter(client=self.get_object())
        else:
            return Invoice.objects.none()

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        invoices = self.get_invoices_set()
        data["invoices"] = invoices
        return data


class ClientUpdateView(LoginRequiredMixin, UpdateView):
    template_name = "edit_client.html"
    fields = [
        "first_name",
        "last_name",
        "email",
        "company",
        "address1",
        "address2",
        "country",
        "phone_number",
    ]

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Client.objects.filter(created_by=self.request.user)
        else:
            return Client.objects.none()


class ClientDeleteView(LoginRequiredMixin, DeleteView):
    template_name = "confirm_delete_client.html"
    success_url = reverse_lazy("client-list")

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Client.objects.filter(created_by=self.request.user)
        else:
            return Client.objects.none()


@login_required
def generate_pdf_invoice(request, invoice_id):
    """Generate PDF Invoice"""

    queryset = Invoice.objects.filter(user=request.user)
    invoice = get_object_or_404(queryset, pk=invoice_id)

    client = invoice.client
    user = invoice.user
    invoice_items = InvoiceItem.objects.filter(invoice=invoice)

    context = {
        "invoice": invoice,
        "client": client,
        "user": user,
        "invoice_items": invoice_items,
        "host": request.get_host(),
    }
    print(request.get_host())

    html_template = render_to_string("pdf/html-invoice.html", context)

    pdf_file = HTML(
        string=html_template, base_url=request.build_absolute_uri()
    ).write_pdf()
    pdf_filename = f"invoice_{invoice.id}.pdf"
    response = HttpResponse(pdf_file, content_type="application/pdf")
    response["Content-Disposition"] = "filename=%s" % (pdf_filename)
    return response


def simple_upload(request):
    if request.method == "POST" and request.FILES["myfile"]:
        myfile = request.FILES["myfile"]
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        return render(
            request, "simple_upload.html", {"uploaded_file_url": uploaded_file_url}
        )
    return render(request, "simple_upload.html")
