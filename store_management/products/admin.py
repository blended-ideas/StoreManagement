from django.contrib import admin

# Register your models here.
from store_management.products.models import Product, ProductExpiry, ProductStockChange


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'stock')
    readonly_fields = ('created_by',)


@admin.register(ProductExpiry)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('product', 'datetime')
    readonly_fields = ('product',)


@admin.register(ProductStockChange)
class ProductStockChangeAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'changeType', 'value')
    list_filter = ('changeType',)
    readonly_fields = ('user', 'product', 'shift_entry')
