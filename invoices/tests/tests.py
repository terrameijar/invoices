import datetime

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from freezegun import freeze_time

from invoices.models import Client, Invoice, InvoiceItem


@freeze_time("2019-01-01")
class InvoiceTests(TestCase):
    def setUp(self):
        # create sample Invoice, Client, and User
        self.user = get_user_model().objects.create_user(
            username="testuser", email="test@email.com", password="secretpassword"
        )

        self.client1 = Client.objects.create(
            first_name="Test",
            last_name="Client",
            email="test@example.com",
            company="Xcorp",
            address1="1234 Paradise Lane",
            address2="Good Street",
            country="Zimbabwe",
            phone_number="+263771811111",
            created_by=self.user,
        )

        self.invoice = Invoice.objects.create(
            title="Test Invoice 1",
            user=self.user,
            client=self.client1,
            create_date=datetime.datetime.now(),
        )

        self.invoice_item1 = InvoiceItem.objects.create(
            invoice=self.invoice,
            item="Test Line Item",
            quantity=3,
            rate=20,
            tax=0,
        )

        self.invoice_item2 = InvoiceItem.objects.create(
            invoice=self.invoice,
            item="Test Line Item 2",
            quantity=1,
            rate=20,
            tax=0,
        )
        self.invoice.save()

    def test_invoice_title(self):
        invoice = Invoice.objects.get(id=self.invoice.id)
        expected_invoice_title = f"{invoice.title}"
        self.assertEqual(expected_invoice_title, "Test Invoice 1")

    def test_invoice_total(self):
        invoice = Invoice.objects.get(id=self.invoice.id)
        self.assertEqual(invoice.get_invoice_total(), 80)

    def test_invoice_str_method(self):
        invoice = Invoice.objects.get(id=self.invoice.id)
        expected_invoice_str = f"{invoice.title} - {invoice.get_invoice_total():.2f}"
        self.assertEqual(expected_invoice_str, "Test Invoice 1 - 80.00")

    def test_invoice_repr_method(self):
        invoice = Invoice.objects.get(id=self.invoice.id)
        expected_invoice_repr = repr(invoice)
        self.assertEqual(
            expected_invoice_repr, "<Invoice: Test Client - Test Invoice 1>"
        )

    def test_invoice_create_date(self):
        invoice = Invoice.objects.get(id=self.invoice.id)
        expected_create_date = invoice.create_date
        self.assertEqual(expected_create_date, datetime.date(2019, 1, 1))

    def test_invoice_client(self):
        invoice = Invoice.objects.get(id=self.invoice.id)
        expected_client = str(invoice.client)
        self.assertEqual(expected_client, "Test Client")

    def test_invoice_contains_client_address(self):
        invoice = Invoice.objects.get(id=self.invoice.id)
        client_address1 = invoice.client.address1
        client_address2 = invoice.client.address2
        self.assertEqual(client_address1, "1234 Paradise Lane")
        self.assertEqual(client_address2, "Good Street")


class ClientTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser", email="test@email.com", password="secretpassword"
        )

        self.client1 = Client.objects.create(
            first_name="Test",
            last_name="Client",
            email="test@example.com",
            company="Xcorp",
            address1="1234 Paradise Lane",
            address2="Good Street",
            country="Zimbabwe",
            phone_number="+263771811111",
            created_by=self.user,
        )

        self.client2 = Client.objects.create(
            first_name="Jane",
            last_name="Doe",
            email="janedoe@example.com",
            company="Cybertron Accounting",
            address1="1234 Energon Lane",
            address2="Oil Street",
            country="Cybertron",
            phone_number="+263771811111",
            created_by=self.user,
        )

        self.invoice = Invoice.objects.create(
            title="Test Invoice 1",
            user=self.user,
            client=self.client1,
            create_date=datetime.datetime.now(),
        )

        self.invoice_item1 = InvoiceItem.objects.create(
            invoice=self.invoice,
            item="Test Line Item",
            quantity=3,
            rate=20,
            tax=0,
        )

        self.invoice_item2 = InvoiceItem.objects.create(
            invoice=self.invoice,
            item="Test Line Item 2",
            quantity=1,
            rate=20,
            tax=0,
        )

        self.invoice2 = Invoice.objects.create(
            title="Test Invoice 2",
            user=self.user,
            client=self.client1,
            create_date=datetime.datetime.now(),
        )

        self.invoice_item1 = InvoiceItem.objects.create(
            invoice=self.invoice2,
            item="Test Line Item",
            quantity=3,
            rate=20,
            tax=0,
        )

        self.invoice_item2 = InvoiceItem.objects.create(
            invoice=self.invoice2,
            item="Test Line Item 2",
            quantity=1,
            rate=20,
            tax=0,
        )

    def test_client_object_content(self):
        client1 = self.client1
        expected_first_name = f"{client1.first_name}"
        expected_last_name = f"{client1.last_name}"

        self.assertEqual(expected_first_name, "Test")
        self.assertEqual(expected_last_name, "Client")

    def test_client_object_repr(self):
        client1 = self.client1
        self.assertEqual(repr(client1), "Client: Test Client")

    def test_client_str(self):
        client1 = self.client1
        self.assertEqual(str(client1), "Test Client")

    def test_client_created_by_returns_correct_user(self):
        client1 = self.client1
        created_by = f"{client1.created_by}"
        self.assertEqual(created_by, "testuser")

    def test_invoices_billed_to_client(self):
        client1 = self.client1
        client2 = self.client2

        invoices_billed_to_client1 = client1.invoice_set.all()
        invoices_billed_to_client2 = client2.invoice_set.all()

        self.assertEqual(len(invoices_billed_to_client1), 2)
        self.assertEqual(len(invoices_billed_to_client2), 0)

    def test_get_absolute_url(self):
        expected_url = f"/clients/{self.client1.id}/"
        self.assertEqual(self.client1.get_absolute_url(), expected_url)


class ViewsLoggedInTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser", email="test@email.com", password="secretpassword"
        )

        self.client1 = Client.objects.create(
            first_name="Test",
            last_name="Client",
            email="test@example.com",
            company="Xcorp",
            address1="1234 Paradise Lane",
            address2="Good Street",
            country="Zimbabwe",
            phone_number="+263771811111",
            created_by=self.user,
        )

        self.client2 = Client.objects.create(
            first_name="Jane",
            last_name="Doe",
            email="doej@example.com",
            company="XYZ Company",
            address1="1234 Paradise Lane",
            address2="Good Street",
            country="Zimbabwe",
            phone_number="+263771811111",
            created_by=self.user,
        )

        self.invoice = Invoice.objects.create(
            title="Test Invoice 1",
            user=self.user,
            client=self.client1,
            create_date=datetime.datetime.now(),
        )

        self.client.login(username="testuser", password="secretpassword")

    def test_homepage_view(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Invoices Landing Page")
        self.assertTemplateUsed(response, "home.html")

    def test_invoice_list_view(self):
        response = self.client.get(reverse("invoice-list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Invoicing App")
        self.assertTemplateUsed(response, "dashboard.html")
        self.assertNotIn("You have not created any invoices yet.", response)

    def test_invoice_create_view(self):
        response = self.client.get(reverse("new-invoice"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "new_invoice.html")

    def test_invoice_detail_view(self):
        response = self.client.get(reverse("invoice-detail", args=[self.invoice.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "invoice_detail.html")

    def test_invoice_update_view(self):
        response = self.client.get(reverse("invoice-edit", args=[self.invoice.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "edit_invoice.html")

    def test_invoice_delete_view(self):
        response = self.client.get(reverse("invoice-delete", args=[self.invoice.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "confirm_delete_invoice.html")

    def test_add_client_view(self):
        response = self.client.get(reverse("new-client"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "new_client.html")

    def test_client_list_view(self):
        response = self.client.get(reverse("client-list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "clients.html")
        self.assertNotIn("You have not created any clients yet.", response)

    def test_client_update_view(self):
        response = self.client.get(reverse("client-edit", args=[self.client1.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "edit_client.html")

    def test_client_detail_view(self):
        response = self.client.get(reverse("client-detail", args=[self.client1.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "client_detail.html")
        search_query = """<table class="table table-hover client-invoices-table">"""
        self.assertIn(search_query, response.content.decode())

    def test_new_client_does_not_have_invoices_billed_to_them(self):
        response = self.client.get(reverse("client-detail", args=[self.client2.id]))
        self.assertIn(
            "You have not billed this customer yet.", response.content.decode()
        )

    def test_client_delete_view(self):
        response = self.client.get(reverse("client-delete", args=[self.client1.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "confirm_delete_client.html")


class ViewsLoggedOutTests(TestCase):
    def test_homepage_view(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)

    def test_invoice_list_view(self):
        response = self.client.get(reverse("invoice-list"))
        self.assertEqual(response.status_code, 302)

    def test_invoice_create_view(self):
        response = self.client.get(reverse("new-invoice"))
        self.assertEqual(response.status_code, 302)

    def test_invoice_detail_view(self):
        response = self.client.get(reverse("invoice-detail", args=[1]))
        self.assertEqual(response.status_code, 302)

    def test_invoice_update_view(self):
        response = self.client.get(reverse("invoice-edit", args=[1]))
        self.assertEqual(response.status_code, 302)

    def test_invoice_delete_view(self):
        response = self.client.get(reverse("invoice-delete", args=[1]))
        self.assertEqual(response.status_code, 302)

    def test_add_client_view(self):
        response = self.client.get(reverse("new-client"))
        self.assertEqual(response.status_code, 302)

    def test_client_list_view(self):
        response = self.client.get(reverse("client-list"))
        self.assertEqual(response.status_code, 302)

    def test_client_update_view(self):
        response = self.client.get(reverse("client-edit", args=[1]))
        self.assertEqual(response.status_code, 302)

    def test_client_detail_view(self):
        response = self.client.get(reverse("client-detail", args=[1]))
        self.assertEqual(response.status_code, 302)

    def test_client_delete_view(self):
        response = self.client.get(reverse("client-detail", args=[1]))
        self.assertEqual(response.status_code, 302)


class ViewsLoggedInNewUserTests(TestCase):
    # These tests test website functionality for a new user who hasn't added
    # any data

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser", email="test@email.com", password="secretpassword"
        )

        self.client.login(username="testuser", password="secretpassword")

    def test_empty_client_list_view(self):
        response = self.client.get(reverse("client-list"))
        self.assertContains(response, "You have not created any clients yet")

    def test_empty_invoice_list_view(self):
        response = self.client.get(reverse("invoice-list"))
        self.assertContains(response, "You have not created any invoices yet.")
