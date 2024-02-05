from django.contrib import admin
from .models import *


@admin.register(CoreUser)
class CoreUseradmin(admin.ModelAdmin):
    list_display = ['first_name','last_name','username']