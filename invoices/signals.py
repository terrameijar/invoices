from django.db.models import F, Sum
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Invoice, InvoiceItem


@receiver(post_save, sender=InvoiceItem)
def set_invoice_total(sender, instance, **kwargs):
    total = instance.invoice.items.aggregate(
        invoice_total=Sum(F("quantity") * F("rate"))
    ).get("invoice_total", 0)
    if total:
        Invoice.objects.filter(pk=instance.invoice.pk).update(invoice_total=total)


@receiver(post_save, sender=Invoice)
def set_invoiceitem_total(sender, instance, **kwargs):
    if len(instance.items.all()) > 0:
        total = instance.items.aggregate(
            invoice_total=Sum(F("quantity") * F("rate"))
        ).get("invoice_total", 0)
        if total:
            Invoice.objects.filter(pk=instance.pk).update(invoice_total=total)
