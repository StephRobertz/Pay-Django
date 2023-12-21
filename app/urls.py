from django.urls import path
from .views import landingview, customerlistview, addcustomer, invoicelistview, addinvoice

urlpatterns = [
    path('', landingview),


    # Customers url's
    path('customerlist/', customerlistview),
    path('add-customer/', addcustomer),


    # Invoice url's
    path('invoicelist/', invoicelistview),
    path('add-invoice/', addinvoice),
]
