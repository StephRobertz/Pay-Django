from django import forms
from .models import CustomerAccount, Account, Invoice, InvoiceRows, Vat
from django.forms import modelformset_factory



class CustomerForm(forms.ModelForm):
    class Meta:
        model = CustomerAccount
        fields = ('name', 'address', 'phone', 'mail', 'vat', 'account')



class InvoiceForm(forms.ModelForm):
    class Meta:
        model = Invoice
        exclude = ['invoiceDate','dueDate']
        fields = ('__all__')

class VatForm(forms.ModelForm):
    class Meta:
        model = Vat
        exclude = ['code','description']
        fields = ('__all__')

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
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Enter title'}),
            'price': forms.NumberInput(attrs={'placeholder': 'Enter price'}),
            'quantity': forms.NumberInput(attrs={'placeholder': 'Enter quantity'}),
            
        }

InvoiceRowFormSet = forms.modelformset_factory(InvoiceRows, form=InvoiceRowForm, extra=1, can_delete=True)

# class InvoiceRowFormSet(forms.models.BaseModelFormSet):
#     def clean(self):
#         super().clean()
#         total = 0

#         for form in self.forms:
#             if form.cleaned_data.get('quantity') and form.cleaned_data.get('price'):
#                 quantity = form.cleaned_data['quantity']
#                 price = form.cleaned_data['price']
#                 # percent = form.cleaned_data['vat'].percent if 'vat' in form.cleaned_data else 0
                
#                 total += quantity * price 

        
#         self.forms[0].instance.total = total


# # Use Django's formsets to handle multiple forms on the same page

# InvoiceRowFormSet = modelformset_factory(InvoiceRows, form=InvoiceRowForm, extra=1)