from django.urls import path
from .views import landingview, customerlistview, addcustomer

urlpatterns = [
    path('', landingview),


    # Customers url's
    path('customerlist/', customerlistview),
    path('add-customer/', addcustomer),
]
