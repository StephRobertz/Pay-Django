from django.urls import path
from .views import landingview, customerlistview, addCustomer, invoicelistview, addInvoice, accountlistview
from .views import deletecustomer, confirmdeletecustomer, edit_customer_get, edit_customer_post,  invoicerowlistview ,edit_invoice_get, edit_invoice_post
from .views import deleteinvoice, confirmdeleteinvoice,  preview_invoice, SendInvoice
from .views import invoices_filtered, GeneratePdf

urlpatterns = [
    path('', landingview),

    path('accountlist/', accountlistview),

    # Customers url's
    path('customerlist/', customerlistview, name="customers"),
    path('add-customer/', addCustomer, name="add-customer"),
    path('delete-customer/<int:id>/', deletecustomer),
    path('confirm-delete-customer/<int:id>/', confirmdeletecustomer),
    path('edit-customer-get/<int:id>/', edit_customer_get),
    path('edit-customer-post/<int:id>/', edit_customer_post),


    # Invoice url's
    path('invoicelist/', invoicelistview, name='invoicelist'),
    path('invoicerowlist/', invoicerowlistview, name='invoicerowlist'),
    path('add-invoice/', addInvoice, name='add-invoice'),
    path('edit-invoice-get/<int:id>/', edit_invoice_get, name='edit_invoice_get'),
    path('edit-invoice-post/<int:id>/', edit_invoice_post, name='edit_invoice_post'),
    path('invoices-by-customer/<int:id>/', invoices_filtered),
    path('delete-invoice/<int:id>/', deleteinvoice),
    path('confirm-delete-invoice/<int:id>/', confirmdeleteinvoice, name='confirm_delete_invoice'),
    path('invoice/<int:id>/preview/', preview_invoice, name='preview_invoice'),
    # path('generate_invoice_pdf/<int:id>/', generate_invoice_pdf, name='generate_invoice_pdf'),
    path('pdf/<int:id>/', GeneratePdf.as_view(), name='generate_pdf'),
    path('send_invoice/<int:id>/', SendInvoice.as_view(), name='send_invoice'),
]
