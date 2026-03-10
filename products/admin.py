from django.contrib import admin

from .models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_id', 'name', 'category', 'price', 'quantity', 'status', 'last_updated')
    list_filter = ('status', 'category')
    search_fields = ('name', 'category', 'product_id')
