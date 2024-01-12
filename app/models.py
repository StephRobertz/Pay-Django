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
    title = models.CharField(max_length = 100, default=None)
    price = models.DecimalField(max_digits = 10, decimal_places=2, default=Decimal('0.00'))
    quantity = models.IntegerField(default = None, null=True)
    total = models.DecimalField(max_digits = 10, decimal_places=2, default=Decimal('0.00'), null=True)
    invoice = models.ForeignKey(Invoice, on_delete =models.CASCADE)
    vat = models.ForeignKey(Vat, on_delete =models.PROTECT, blank=True, null=True)

    def __str__(self):
        return self.title
    
   
    
    def calc_total(self):
        # Convert the price and quantity to numeric types before multiplication
        price_numeric = float(self.price)
        quantity_numeric = float(self.quantity) if self.quantity is not None else 0

        amount = Decimal(price_numeric) * Decimal(quantity_numeric)

        
        return amount

    def save(self, *args, **kwargs):
        self.total = self.calc_total()
        super(InvoiceRows, self).save(*args, **kwargs)


# def calc_total(self):
#         # Convert the price and quantity to Decimal directly
#         price_decimal = Decimal(self.price)
#         quantity_decimal = Decimal(self.quantity) if self.quantity is not None else Decimal('0')

#         # Check if there is a VAT associated with the row
#         vat_percent = self.vat.percent if self.vat else 0.0

#         # Calculate the amount including VAT
#         amount = price_decimal * quantity_decimal * (1 + vat_percent / 100)

#         return amount

# def save(self, *args, **kwargs):
#         self.total = self.calc_total()
#         super(InvoiceRows, self).save(*args, **kwargs)
