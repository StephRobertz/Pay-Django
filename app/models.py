from django.db import models
from datetime import datetime, timedelta

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
        return f"{self.name} - {self.id}"

class Invoice(models.Model):
    invoiceDate = models.DateTimeField(auto_now_add=True)
    dueDate = models.DateTimeField(default=datetime.now() + timedelta(days=14)) #time + 14 days
    customerAccount = models.ForeignKey(CustomerAccount, on_delete =models.PROTECT)
    account = models.ForeignKey(Account, on_delete =models.PROTECT)

    def __str__(self):
        return f"{self.id} - {self.dueDate}"
    
class Vat(models.Model):
    code = models.CharField(max_length = 50, default="M24")
    description = models.CharField (max_length = 50, default="VAT (Value Added Tax @ 24%)")
    percent = models.DecimalField(max_digits = 5, decimal_places=2, default="24%")

    def __str__(self):
        return self.description

class InvoiceRows(models.Model):
    title = models.CharField(max_length = 100, default=None)
    price = models.DecimalField(max_digits = 10, decimal_places=2, default=None)
    quantity = models.IntegerField(default = None)
    total = models.DecimalField(max_digits = 10, decimal_places=2, default=None)
    invoice = models.ForeignKey(Invoice, on_delete =models.PROTECT)
    vat = models.ForeignKey(Vat, on_delete =models.PROTECT)

    def __str__(self):
        return self.title



