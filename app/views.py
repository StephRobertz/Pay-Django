from django.shortcuts import render, redirect
from .models import CustomerAccount, Invoice, InvoiceRows, Account
from .forms import CustomerForm, InvoiceForm, InvoiceRowFormSet, InvoiceRowForm
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from django.views.generic import View
from django.views import View
from .process import html_to_pdf
from django.forms import modelformset_factory
from django.http import HttpResponse
from django.core.mail import send_mail


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
            # Tallentaa lomakkeen, + valittu tili (Account)
            customer = form.save(commit=False)

            selected_account = request.POST.get('account')

            # Hakee valittu tili
            try:
                account = Account.objects.get(id=selected_account)
            except Account.DoesNotExist:
              
                return render(request, 'customeradd.html', {'form': form, 'error_message': 'Selected Account does not exist'})

            # Liittää valittu tili asiakkaaseen
            customer.account = account

            customer.save()

            return redirect(customerlistview)  # Ohjaa asiakasnäkymään
    else:
        form = CustomerForm()

    return render(request, 'customeradd.html', {'form': form})





def confirmdeletecustomer(request, id):
    customer = CustomerAccount.objects.get(id = id)
    context = {'customer': customer}
    return render (request,"custdeleteconfirm.html",context)


def deletecustomer(request, id):
    try:
        customer = CustomerAccount.objects.get(id = id)
        context = {'customer': customer}
        # Tarkistaa onko asiakkaalla olemassa olevia laskuja
        if Invoice.objects.filter(customerAccount=customer).exists():
            return render(request, "custdelerror.html",context)
       
        customer.delete()
        return redirect(customerlistview)
    
    
    except Exception as e:
        # Vianmääritystä varten
        import traceback
        traceback.print_exc()
        return render(request, "custdelerror.html", {'error_message': "An error occurred while processing the request."})
    
# def deletecustomer(request, id):
#     try:
#         CustomerAccount.objects.get(id = id).delete()
#         return redirect(customerlistview)
#     except Exception as e:
#          # Vianmääritystä varten
#         import traceback
#         traceback.print_exc()
        
#     return HttpResponse("An error occurred while processing the request. Cannot delete customer because of existing invoices.", status=500)


def edit_customer_get(request, id):
    customer = get_object_or_404(CustomerAccount, id=id)
    context = {'customer': customer}
    return render(request, "customeredit.html", context)

def edit_customer_post(request, id):
    customer = get_object_or_404(CustomerAccount, id=id)

    if request.method == 'POST':
        customer.name = request.POST.get('name')
        customer.address = request.POST.get('address')
        customer.phone = request.POST.get('phone')
        customer.mail = request.POST.get('mail')
        customer.vat = request.POST.get('vat')
        customer.save()
        return redirect(customerlistview)



#INVOICE VIEWS
 

#Listaus

def invoicelistview(request):
    invoices = Invoice.objects.all().order_by('-invoiceDate')
    context = {'invoices': invoices}
    return render(request, "invoicelist.html", context)

def invoicerowlistview(request):
    invoicerowlist = InvoiceRows.objects.all()
    invoicelist = Invoice.objects.all()
    context = {'invoicerow': invoicerowlist, 'invoices': invoicelist}
    return render (request,"invoicerowlist.html", context)


#Muokkaus

#Luo lomakesarja (formset) käyttäen modelformset_factory-funktiota.
#Lomakesarja('formset') käytetään monien lomakkeiden käsittelyyn samalla sivulla.

#(modelformset_factory)  handle multiple instances of the model in a single view or form.
InvoiceRowFormSet = modelformset_factory(InvoiceRows, form=InvoiceRowForm, extra=0)

def edit_invoice_get(request, id):
    invoices = get_object_or_404(Invoice, id=id)
    invoicerow = InvoiceRows.objects.filter(invoice=invoices)   # Hakee laskuun liittyvät laskurivit.
    formset = InvoiceRowFormSet(queryset=invoicerow)         # Luo lomakesarja haetuille laskuriveille.


    context = {'invoice': invoices, 'formset': formset}
    return render(request, "invoiceedit.html", context)


def edit_invoice_post(request, id):
    invoice = get_object_or_404(Invoice, id=id)
    invoicerows = InvoiceRows.objects.filter(invoice=invoice)
    formset = InvoiceRowFormSet(request.POST, queryset=invoicerows)

    if formset.is_valid():
        instances = formset.save(commit=False)   # Tallenna tietokantaan, mutta ei tee niistä välitöntä sitoutumista (commit = False). (commit = False)Tämä on hyödyllistä, kun haluat suorittaa lisätoimia, ennen niiden tallentamista tietokantaan.
        for instance in instances:              # Käydään läpi kaikki laskurivit, varmistaen, että jokainen rivi on yhdistetty vastaavaan laskuun.
            instance.invoice = invoice
            instance.save()

        formset.save_m2m()                  # Save any many-to-many relationships

        return redirect('preview_invoice', id=invoice.id) 
    else:
        print("Formset is not valid")
        print(formset.errors)


    context = {'invoice': invoice, 'formset': formset}
    return render(request, "invoiceedit.html", context)



#Lisäys

def addInvoice(request):
    # Luo formsetin uusien rivien lisäämistä varten.
    AddInvoiceRowFormSet = modelformset_factory(InvoiceRows, form=InvoiceRowForm, extra=1)

    if request.method == 'POST':
        form = InvoiceForm(request.POST)
        formset = AddInvoiceRowFormSet(request.POST, queryset=InvoiceRows.objects.none(), prefix='invoicerow')

        if form.is_valid() and formset.is_valid():
            invoices = form.save()
            invoicerow = formset.save(commit=False)

            total = 0
            for row in invoicerow:
                # Liitä jokainen rivi laskuun.
                row.invoice = invoices
                row.save()

                # Laske summa kullekin riville.
                total += row.quantity * row.price

            invoices.total = total
            invoices.save()

            return redirect('preview_invoice', id=invoices.id)
    else:
        form = InvoiceForm()
        formset = AddInvoiceRowFormSet(queryset=InvoiceRows.objects.none(), prefix='invoicerow')

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
        # Hakee data tietokannasta
        invoice_instance = get_object_or_404(Invoice, id=id)
        invoice_rows = InvoiceRows.objects.filter(invoice=invoice_instance)

        # Laskun tiedot
        invoice_data = {
            'invoice_id': invoice_instance.id,
            'date': invoice_instance.invoiceDate,
            'customer': invoice_instance.customerAccount.name,
            'items': [
                {'description': ir.title, 'quantity': ir.quantity, 'unit_price': ir.price, 'total': ir.total, 'total_with_tax': ir.total_with_tax}
                for ir in invoice_rows
            ],
        }

        # Hakee muita liittyviä tietoja esikatselua varten.
        invoicelist = Invoice.objects.all()

        context = {
            'invoice': invoice_data,
            'invoicerow': invoice_rows,
            'invoices': invoicelist,
          
        }

        return render(request, 'invoice_preview.html', context)
    
    except Exception as e:
         # Vianmääritystä varten
        import traceback
        traceback.print_exc()
        
        return HttpResponse("An error occurred while processing the request.", status=500)


#PDF generator
#Luodaan luokkapohjainen näkymä
class GeneratePdf(View):
    def get(self, request, id):
        
        invoice_instance = get_object_or_404(Invoice, id=id)
        invoice_rows = InvoiceRows.objects.filter(invoice=invoice_instance)


        # Laskun tiedot
        invoice_data = {
            'invoice_id': invoice_instance.id,
            'date': invoice_instance.invoiceDate,
            'customer': invoice_instance.customerAccount.name,
            'items': [
                {'description': ir.title, 'quantity': ir.quantity, 'unit_price': ir.price, 'total': ir.total}
                for ir in invoice_rows
            ],
        }

        context = {'invoice': invoice_data, 'invoicerow': invoice_rows}
        pdf = html_to_pdf('invoice_template.html', context)

        return HttpResponse(pdf, content_type='application/pdf')
    

    #Send invoice
class SendInvoice(View):
    def get(self, request, id):
        try:
            # Get the invoice data from the database
            invoice_instance = get_object_or_404(Invoice, id=id)
           
            
            # Retrieve customer email
            to_email = invoice_instance.customerAccount.mail

            # Define subject, message, and from_email before using them
            subject = 'Invoice'
            message = 'Please find attached invoice.'
            from_email = 'your-email@gmail.com'

            # Print the email content to the console
            print(f"Email Content:\nSubject: {subject}\nMessage: {message}\nTo: {to_email}")

            # Send mail with fail_silently=True to capture email content
            send_mail(
                subject,
                message,
                from_email,
                [to_email],
                fail_silently=True,
                
            )

            return HttpResponse("Email content printed. Review the console.")
        
        except Exception as e:
            # Error handling
            return HttpResponse(f"An error occurred: {str(e)}", status=500)