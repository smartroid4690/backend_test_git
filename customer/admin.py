from django.contrib import admin
from .models import *



admin.site.register(Address)

@admin.register(Customer)
class Customeradmin(admin.ModelAdmin):
    list_display = ['email','phone_no']
    
@admin.register(Country)
class Countryadmin(admin.ModelAdmin):
    list_display = ['countryName','countryCode','currencyCode','telephonePrefix']
    
    

@admin.register(City)
class Cityadmin(admin.ModelAdmin):
    list_display = ['name','country_id']
    list_filter = ['country_id']
    