from django.shortcuts import render

def landingview(request):
    return render(request, 'landingpage.html')

def addcustomer(request):
    return render(request, 'customeradd.html')

def customerlistview(request):
    return render(request, 'customerlist.html')
