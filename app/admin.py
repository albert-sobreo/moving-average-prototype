from django.contrib import admin
from .models import Inventory, Purchase, Sales
# Register your models here.

admin.site.register(Inventory)
admin.site.register(Purchase)
admin.site.register(Sales)