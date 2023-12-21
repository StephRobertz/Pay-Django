# Register your models here.
# Jos rekisteröi tällä tavalla adminille oman appin
# modelit, voi myös admin sivuilta muokata näitä tietoja.

from django.contrib import admin

from app.models import Account, CustomerAccount, Vat

@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    pass

@admin.register(CustomerAccount)
class CustomerAccountAdmin(admin.ModelAdmin):
    pass

@admin.register(Vat)
class VatAdmin(admin.ModelAdmin):
    pass