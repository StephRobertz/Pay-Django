from django.urls import path
from .views import landingview, customerlistview, addCustomer, invoicelistview, addInvoice, accountlistview
from .views import deletecustomer, confirmdeletecustomer, edit_customer_get, edit_customer_post,  invoicerowlistview

urlpatterns = [
    path('', landingview),

    path('accountlist/', accountlistview),

    # Customers url's
    path('customerlist/', customerlistview),
    path('add-customer/', addCustomer, name="add-customer"),
    path('delete-customer/<int:id>/', deletecustomer),
    path('confirm-delete-customer/<int:id>/', confirmdeletecustomer),
    path('edit-customer-get/<int:id>/', edit_customer_get),
    path('edit-customer-post/<int:id>/', edit_customer_post),


    # Invoice url's
    path('invoicelist/', invoicelistview, name='invoicelist'),
    path('invoicerowlist/', invoicerowlistview, name='invoicerowlist'),
    path('add-invoice/', addInvoice, name="add-invoice"),
]
