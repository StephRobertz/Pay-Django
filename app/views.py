from django.shortcuts import render
from .models import CustomerAccount, Invoice

def landingview(request):
    return render(request, 'landingpage.html')


#CUSTOMERS VIEWS

def addcustomer(request):
    return render(request, 'customeradd.html')


def customerlistview(request):
    customerlist = CustomerAccount.objects.all()
    context = {'customers': customerlist}
    return render (request,"customerlist.html",context)


#INVOICE VIEWS
 
def addinvoice(request):
    return render(request, 'invoiceadd.html')

def invoicelistview(request):
    invoicelist = Invoice.objects.all()
    customerlist = CustomerAccount.objects.all()
    context = {'invoices': invoicelist, 'customers': customerlist}
    return render (request,"invoicelist.html",context)