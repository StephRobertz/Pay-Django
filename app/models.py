from django.db import models
from datetime import datetime, timedelta
from decimal import Decimal

class Account(models.Model):
    name = models.CharField(max_length =20, default=None)
    address = models.CharField(max_length =50, default=None)
    phone = models.CharField(max_length =50, default=None)
    mail = models.CharField(max_length =50, default=None)
    vat = models.CharField(max_length =20, default=None)
    bankAccountNr = models.CharField(max_length =20, default=None)

    def __str__(self):
        return self.name

class CustomerAccount(models.Model):
    name = models.CharField(max_length = 50, default=None)
    address = models.CharField(max_length = 50, default=None)
    phone = models.CharField(max_length = 50, default=None)
    mail = models.CharField(max_length = 50, default=None)
    vat = models.CharField(max_length = 20, default=None)
    account = models.ForeignKey(Account, on_delete =models.PROTECT)

    def __str__(self):
        return f"{self.name} - ID: {self.id}"

class Invoice(models.Model):
    invoiceDate = models.DateTimeField(auto_now_add=True)
    dueDate = models.DateTimeField(default=datetime.now() + timedelta(days=14)) #time + 14 days
    customerAccount = models.ForeignKey(CustomerAccount, on_delete =models.PROTECT)
    account = models.ForeignKey(Account, on_delete =models.PROTECT)

    def __str__(self):
        return f"ID: {self.id} - {self.dueDate}"
    
class Vat(models.Model):
    code = models.CharField(max_length = 50, default="M24")
    description = models.CharField (max_length = 50, default="VAT (Value Added Tax @ 24%)")
    percent = models.DecimalField(max_digits = 5, decimal_places=2, default=Decimal('0.24'))

    def __str__(self):
        return self.description

class InvoiceRows(models.Model):
    title = models.CharField(max_length = 100, default=None, blank=True, null=True)
    price = models.DecimalField(max_digits = 10, decimal_places=2, default=Decimal('0.00'), blank=True, null=True)
    quantity = models.IntegerField(default = 0, null=True)
    total = models.DecimalField(max_digits = 10, decimal_places=2, default=Decimal('0.00'), null=True)
    total_with_tax = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'), null=True)
    invoice = models.ForeignKey(Invoice, on_delete =models.CASCADE)
    vat = models.ForeignKey(Vat, on_delete =models.PROTECT, blank=True, null=True)

    def __str__(self):
        return self.title
    
   
    
    def calc_total(self):
        # Convert the price and quantity to numeric types before multiplication
        price = float(self.price)
        quantity = float(self.quantity) if self.quantity is not None else 0

        amount = Decimal(price) * Decimal(quantity)
        return amount


    def save(self, *args, **kwargs):
        self.total = self.calc_total()
        self.vat_amount = self.total * (self.vat.percent / 100 if self.vat else Decimal('0.00'))

        print(f"Debug: total={self.total}, vat_amount={self.vat_amount}")
        self.total_with_tax = self.total + self.vat_amount
        print(f"Debug: total={self.total}, vat_amount={self.vat_amount}, total_with_tax={self.total_with_tax}")  # Add this line for debugging
        super(InvoiceRows, self).save(*args, **kwargs)

   