
# Register your models here.
# PriceDropAlert/admin.py
from django.contrib import admin
from .models import PriceDropAlert

@admin.register(PriceDropAlert)
class PriceDropAlertAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'product', 'target_price', 'email', 'active')
    list_filter = ('active',)
    search_fields = ('user__username', 'product__name', 'email')
