from django.shortcuts import render, redirect
from django.urls import reverse, path
from .models import CustomerAccount, Invoice, InvoiceRows, Account
from .forms import CustomerForm, InvoiceForm, InvoiceRowFormSet, InvoiceRowForm

from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from django.db.models import Sum
from django.views.generic import View
from .process import html_to_pdf
from django.views import View
from django.forms import modelformset_factory

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
InvoiceRowFormSet = modelformset_factory(InvoiceRows, form=InvoiceRowForm, extra=1)
def edit_invoice_get(request, id):
    invoices = get_object_or_404(Invoice, id=id)
    invoicerow = InvoiceRows.objects.filter(invoice=invoices)
    formset = InvoiceRowFormSet(queryset=invoicerow)

    context = {'invoice': invoices, 'formset': formset}
    return render(request, "invoiceedit.html", context)


def edit_invoice_post(request, id):
    invoice = get_object_or_404(Invoice, id=id)
    invoicerows = InvoiceRows.objects.filter(invoice=invoice)
    formset = InvoiceRowFormSet(request.POST, queryset=invoicerows)

    if formset.is_valid():
        instances = formset.save(commit=False)
        for instance in instances:
            instance.invoice = invoice
            instance.save()

        formset.save_m2m()

        return redirect('invoicelist') 
    else:
        print("Formset is not valid")
        print(formset.errors)

    context = {'invoice': invoice, 'formset': formset}
    return render(request, "invoiceedit.html", context)





# def edit_invoice_post(request, id):
#     print(f"Processing edit_invoice_post for id: {id}")
#     invoices = get_object_or_404(Invoice, id=id)
#     invoicerow = InvoiceRows.objects.filter(invoice=invoices)
#     formset = InvoiceRowFormSet(request.POST, queryset=invoicerow)

#     if formset.is_valid():
#         formset.save()
#     print("Redirecting to invoicelist")
#     return redirect(invoicelistview)



#add
def addInvoice(request):
    if request.method == 'POST':
        form = InvoiceForm(request.POST)
        formset = InvoiceRowFormSet(request.POST, queryset=InvoiceRows.objects.none(), prefix='invoicerow') #formset is a layer of abstraction to work with multiple forms on the same page. 

        if form.is_valid() and formset.is_valid():
            invoices = form.save()
            invoicerow = formset.save(commit=False)

            total = 0
            for row in invoicerow:
                row.invoice = invoices
                row.save()
            
            # Calculate total for each row
                row_total = row.quantity * row.price
                total += row_total

            invoices.total = total
            invoices.save()

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



#PDF preview

def preview_invoice(request, id):
    try:
        # Get the invoice data from the database
        invoice_instance = get_object_or_404(Invoice, id=id)
        invoice_rows = InvoiceRows.objects.filter(invoice=invoice_instance)

        # Calculate total using aggregation
        total = invoice_rows.aggregate(Sum('total'))['total__sum']

        # Your data for the invoice
        invoice_data = {
            'invoice_id': invoice_instance.id,
            'date': invoice_instance.invoiceDate,
            'customer': invoice_instance.customerAccount.name,
            'items': [
                {'description': ir.title, 'quantity': ir.quantity, 'unit_price': ir.price, 'total': ir.total}
                for ir in invoice_rows
            ],
             'total': total,
        }

        # Fetch other related data for preview, if needed
        # invoicerowlist = InvoiceRows.objects.all()
        invoicelist = Invoice.objects.all()

        context = {
            'invoice': invoice_data,
            'invoicerow': invoice_rows,
            'invoices': invoicelist,
        }

        return render(request, 'invoice_preview.html', context)
    
    except Exception as e:
         # Print the exception traceback to the console for debugging
        import traceback
        traceback.print_exc()
        
        # Return an HttpResponse with an error message or redirect to an error page
        return HttpResponse("An error occurred while processing the request.", status=500)


#PDF generator
#Creating a class based view
class GeneratePdf(View):
    def get(self, request, id):
        # Get the invoice data from the database
        invoice_instance = get_object_or_404(Invoice, id=id)
        invoice_rows = InvoiceRows.objects.filter(invoice=invoice_instance)

        # Calculate total using aggregation
        total = invoice_rows.aggregate(Sum('total'))['total__sum']

        # Your data for the invoice
        invoice_data = {
            'invoice_id': invoice_instance.id,
            'date': invoice_instance.invoiceDate,
            'customer': invoice_instance.customerAccount.name,
            'items': [
                {'description': ir.title, 'quantity': ir.quantity, 'unit_price': ir.price, 'total': ir.total}
                for ir in invoice_rows
            ],
            'total': total,
        }

        context = {'invoice': invoice_data, 'invoicerow': invoice_rows}
        pdf = html_to_pdf('invoice_template.html', context)

        return HttpResponse(pdf, content_type='application/pdf')
