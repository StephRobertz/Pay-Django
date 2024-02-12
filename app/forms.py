from django import forms
from .models import CustomerAccount, Invoice, InvoiceRows, Vat




class CustomerForm(forms.ModelForm):
    class Meta:
        model = CustomerAccount
        fields = ('name', 'address', 'phone', 'mail', 'vat', 'account')



class InvoiceForm(forms.ModelForm):
    class Meta:
        model = Invoice
        exclude = ['invoiceDate','dueDate']
        #fields = ('__all__')

class VatForm(forms.ModelForm):
    class Meta:
        model = Vat
        exclude = ['code','description']
        #fields = ('__all__')

class InvoiceRowForm(forms.ModelForm):
   class Meta:
        model = InvoiceRows
        fields = ['title', 'price', 'quantity', 'vat']
        labels = {
            'title': 'Title',
            'price': 'Price',
            'quantity': 'Quantity',
            'vat': 'Vat',
        }
        def __init__(self, *args, **kwargs):        #when creating a subclass that extends the functionality of a parent class.
             super().__init__(*args, **kwargs)
           

        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Enter title'}),
            'price': forms.TextInput(attrs={'placeholder': 'Enter price', 'type': 'number'}),
            'quantity': forms.TextInput(attrs={'placeholder': 'Enter quantity', 'type': 'number'}),
        }
       

InvoiceRowFormSet = forms.modelformset_factory(InvoiceRows, form=InvoiceRowForm, extra=1, can_delete=True)

