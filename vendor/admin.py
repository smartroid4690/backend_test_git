from django.contrib import admin
from .models import *

# Register your models here.


admin.site.register(Market)
admin.site.register(Product)
admin.site.register(Product_image)
admin.site.register(Shop)
admin.site.register(Category)
admin.site.register(Shop_outlet)
admin.site.register(Variation)
admin.site.register(Variation_option)


@admin.register(Vendor)
class Vendoradmin(admin.ModelAdmin):
    list_display = ['email','phone_no']