from django.contrib import admin

# Register your models here.
# products/admin.py

from .models import Product

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_id', 'name', 'platform', 'price', 'store_name')
    search_fields = ('product_id', 'name', 'store_name')
