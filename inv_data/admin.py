from django.contrib import admin

# Register your models here.

from django.contrib import admin
from .models import Category, Product, StockTransaction, StockTransactionItem, Store , Supplier , ImportedFor , Inventory
admin.site.register(Product)
admin.site.register(StockTransaction)
admin.site.register(StockTransactionItem)
admin.site.register(Store)
admin.site.register(Category)
admin.site.register(Supplier)
admin.site.register(ImportedFor)
admin.site.register(Inventory)