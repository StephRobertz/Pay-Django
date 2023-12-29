from django.shortcuts import render, redirect
from .models import CustomerAccount, Invoice, InvoiceRows, Account
from .forms import CustomerForm, InvoiceForm, InvoiceRowFormSet


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

            # Assuming you have a field in your form named 'selected_account'
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
        customer = CustomerAccount.objects.get(id = id)
        context = {'customer': customer}
        return render (request,"customeredit.html",context)


def edit_customer_post(request, id):
        item = CustomerAccount.objects.get(id = id)
        item.name = request.POST['name']
        item.address = request.POST['address']
        item.save()
        return redirect(customerlistview)




#INVOICE VIEWS
 


def invoicelistview(request):
    invoicelist = Invoice.objects.all()
    invoicerowlist = InvoiceRows.objects.all()
    customerlist = CustomerAccount.objects.all()
    accountlist = Account.objects.all()
    context = {'invoices': invoicelist,'invoicerow': invoicerowlist, 'customers': customerlist, 'accounts': accountlist}
    return render (request,"invoicelist.html",context)

def invoicerowlistview(request):
    invoicerowlist = InvoiceRows.objects.all()
    context = {'invoicerow': invoicerowlist}
    return render (request,"invoicerowlist.html",context)


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