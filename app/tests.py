from decimal import Decimal
from django.test import TestCase
from app.models import InvoiceRows, Vat, Invoice, Account, CustomerAccount

class InvoiceRowsTestCase(TestCase):
    def setUp(self):
        # Create sample instances for testing
        self.sample_account = Account.objects.create(
            name="Sample Customer", 
            address="Sample Address", 
            phone="Sample Phone", 
            mail="Sample Mail", 
            vat="Sample Vat", 
            bankAccountNr="Sample Bank")

        self.sample_customer_account = CustomerAccount.objects.create(
            name="Sample Customer", 
            address="Sample Address", 
            phone="Sample Phone", 
            mail="Sample Mail", 
            vat="Sample Vat",
            account=self.sample_account)  # Set the account field

        self.sample_vat = Vat.objects.create(percent=24)  # Adjust percent accordingly

    def test_vat_amount_calculation(self):
        # Create a sample Invoice instance
        sample_invoice = Invoice.objects.create(
            customerAccount=self.sample_customer_account,
            account=self.sample_account
        )

        # Create an InvoiceRows instance and associate it with the sample Invoice
        invoice_row = InvoiceRows.objects.create(
            title='Verkkosivu',
            price=10,
            quantity=8,
            vat=self.sample_vat,
            invoice=sample_invoice  # Set the invoice field
        )

        # Check if vat_amount is calculated correctly after saving
        expected_vat_amount = Decimal('19.20')
        self.assertEqual(invoice_row.vat_amount, expected_vat_amount)

        # Check if total_with_tax is calculated correctly after saving
        expected_total_with_tax = Decimal('99.20')
        self.assertEqual(invoice_row.total_with_tax, expected_total_with_tax)
