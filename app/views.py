from django.shortcuts import render, redirect
from django.urls import reverse
from .models import CustomerAccount, Invoice, InvoiceRows, Account
from .forms import CustomerForm, InvoiceForm, InvoiceRowFormSet, InvoiceRowForm
from django.shortcuts import get_object_or_404
from decimal import Decimal
from django.http import HttpResponseNotFound


def landingview(request):
    return render(request, 'landingpage.html')

#ACCOUNT
def accountlistview(request):
    accountlist = Account.objects.all()
    context = {'accounts': accountlist}
    return render (request,"accountlist.html",context)

#CUSTOMERS VIEWS

def customerlistview(request):
    customerlist = CustomerAccount.objects.all()
    accountlist = Account.objects.all()
    context = {'customers': customerlist, 'accounts': accountlist}
    return render (request,"customerlist.html",context )




def addCustomer(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            # Save the form, including the selected Account
            customer_instance = form.save(commit=False)

            
            selected_account_id = request.POST.get('account')

            # Get the selected Account instance
            try:
                account_instance = Account.objects.get(id=selected_account_id)
            except Account.DoesNotExist:
                # Handle the case where the selected Account doesn't exist
                return render(request, 'customeradd.html', {'form': form, 'error_message': 'Selected Account does not exist'})

            # Associate the selected Account with the Customer
            customer_instance.account = account_instance

            # Save the Customer instance with the associated Account
            customer_instance.save()

            return redirect(customerlistview)  # Redirect to a success page or another view
    else:
        form = CustomerForm()

    return render(request, 'customeradd.html', {'form': form})





def confirmdeletecustomer(request, id):
    customer = CustomerAccount.objects.get(id = id)
    context = {'customer': customer}
    return render (request,"custdeleteconfirm.html",context)


def deletecustomer(request, id):
    CustomerAccount.objects.get(id = id).delete()
    return redirect(customerlistview)

def edit_customer_get(request, id):
    customer = get_object_or_404(CustomerAccount, id=id)
    context = {'customer': customer}
    return render(request, "customeredit.html", context)

def edit_customer_post(request, id):
    customer = get_object_or_404(CustomerAccount, id=id)

    if request.method == 'POST':
        customer.name = request.POST.get('name', '')
        customer.address = request.POST.get('address', '')
        customer.save()

    return redirect(customerlistview)
# def edit_customer_get(request, id):
#         customer = CustomerAccount.objects.get(id = id)
#         context = {'customer': customer}
#         return render (request,"customeredit.html",context)


# def edit_customer_post(request, id):
#         item = CustomerAccount.objects.get(id = id)
#         item.name = request.POST['name']
#         item.address = request.POST['address']
#         item.save()
#         return redirect(customerlistview)




#INVOICE VIEWS
 

#listaus

# def invoicelistview(request):
#     invoicelist = Invoice.objects.all()
#     invoicerowlist = InvoiceRows.objects.all()
#     customerlist = CustomerAccount.objects.all()
#     accountlist = Account.objects.all()
#     context = {'invoices': invoicelist,'invoicerow': invoicerowlist, 'customers': customerlist, 'accounts': accountlist}
#     return render (request,"invoicelist.html",context)
def invoicelistview(request):
    invoices = Invoice.objects.all()
    context = {'invoices': invoices}
    return render(request, "invoicelist.html", context)

def invoicerowlistview(request):
    invoicerowlist = InvoiceRows.objects.all()
    invoicelist = Invoice.objects.all()
    context = {'invoicerow': invoicerowlist, 'invoices': invoicelist}
    return render (request,"invoicerowlist.html", context)


#edit

# def edit_invoice(request, id):
#     # Retrieve the invoice
#     invoice = get_object_or_404(Invoice, id=id)
    
#     # Fetch existing rows related to the invoice
#     invoicerows = InvoiceRows.objects.filter(invoice=invoice)

#     # Handle the formset
#     if request.method == 'POST':
#         formset = InvoiceRowFormSet(request.POST, queryset=invoicerows)
#         if formset.is_valid():
#             # Save the formset
#             formset.save()
#             return redirect('invoicerows', id=id)
#     else:
#         # Create formset with existing rows
#         formset = InvoiceRowFormSet(queryset=invoicerows)

#     return render(request, 'invoiceedit.html', {'formset': formset, 'invoice': invoice})

# def edit_invoice_get(request, id):
#     invoice = get_object_or_404(Invoice, id=id)
#     invoicerows = InvoiceRows.objects.filter(invoice=invoice)
#     context = {'invoice': invoice, 'invoicerows': invoicerows}
#     return render(request, "invoiceedit.html", context)

# def edit_invoice_post(request, id):
#     invoice = get_object_or_404(Invoice, id=id)

#     if request.method == 'POST':
#         form = InvoiceRowForm(request.POST)
#         if form.is_valid():
#             invoicerow = form.save(commit=False)
#             invoicerow.invoice = invoice
#             invoicerow.save()
#             return redirect('edit_invoice_get', id=id)
#     else:
#         form = InvoiceRowForm()

#     return render(request, 'invoiceedit.html', {'form': form, 'invoice': invoice})

# def edit_invoice_get(request, id):
#     invoicerow = InvoiceRows.objects.all
#     invoice = Invoice.objects.get(id=id)
#     context = {'invoicerow': invoicerow,'invoices': invoice}
#     return render (request,"invoiceedit.html", context)
    
    

# def edit_invoice_post(request, id):
#         invoicerow = Invoice.objects.get(id=id)
#         invoicerow = InvoiceRows.objects.all
#         invoicerow.title = request.POST['title']
#         invoicerow.price = request.POST['price']
#         invoicerow.quantity = request.POST['quantity']
#         invoicerow.save()
#         return redirect(invoicerowlistview)
def edit_invoice_get(request, id):
    invoice = get_object_or_404(Invoice, id=id)
    invoicerows = InvoiceRows.objects.filter(invoice=invoice)
    formset = InvoiceRowFormSet(queryset=invoicerows)

    context = {'invoice': invoice, 'formset': formset}
    return render(request, "invoiceedit.html", context)

def edit_invoice_post(request, id):
    invoice = get_object_or_404(Invoice, id=id)
    invoicerows = InvoiceRows.objects.filter(invoice=invoice)
    formset = InvoiceRowFormSet(request.POST, queryset=invoicerows)

    if formset.is_valid():
        formset.save()

    return redirect(reverse('invoicerowlist'))



# def edit_invoice_get(request, id):
#     invoicerows = InvoiceRows.objects.filter(invoice__id=id)
#     invoice = get_object_or_404(Invoice, id=id)
#     context = {'invoicerows': invoicerows, 'invoice': invoice}
#     return render(request, "invoiceedit.html", context)

# def edit_invoice_post(request, id):
#     invoice = get_object_or_404(Invoice, id=id)
#     invoicerows = InvoiceRows.objects.filter(invoice=invoice)

#     for invoicerow in invoicerows:
#         invoicerow.title = request.POST.get(f'title_{invoicerow.id}')
#         invoicerow.price = request.POST.get(f'price_{invoicerow.id}')
#         invoicerow.quantity = request.POST.get(f'quantity_{invoicerow.id}')
#         invoicerow.save()

#     return redirect('invoicerowlistview')

#add
def addInvoice(request):
    if request.method == 'POST':
        form = InvoiceForm(request.POST)
        formset = InvoiceRowFormSet(request.POST, queryset=InvoiceRows.objects.none(), prefix='invoicerow') #formset is a layer of abstraction to work with multiple forms on the same page. 

        if form.is_valid() and formset.is_valid():
            invoice = form.save()
            invoice_rows = formset.save(commit=False)

            total = 0
            for row in invoice_rows:
                row.invoice = invoice
                row.save()
            
            # Calculate total for each row
                row_total = row.quantity * row.price
                total += row_total

            invoice.total = total
            invoice.save()

            return redirect('invoicelist')  # Redirect to a page displaying a list of invoices
    else:
        form = InvoiceForm()
        formset = InvoiceRowFormSet(queryset=InvoiceRows.objects.none(), prefix='invoicerow')

    return render(request, 'invoiceadd.html', {'form': form, 'formset': formset})




def invoices_filtered(request, id):
    invoicelist = Invoice.objects.all()
    filteredinvoices = invoicelist.filter(customerAccount = id)
    context = {'invoices': filteredinvoices}
    return render (request,"invoicelist.html",context)

def confirmdeleteinvoice(request, id):
    invoice = Invoice.objects.get(id = id)
    context = {'invoice': invoice}
    return render (request,"invoicedelconfirm.html",context)


def deleteinvoice(request, id):
    Invoice.objects.get(id = id).delete()
    return redirect(invoicelistview)