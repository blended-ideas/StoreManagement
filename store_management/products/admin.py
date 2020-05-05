from django.contrib import admin

# Register your models here.
from store_management.products.models import Product, ProductExpiry


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'username')
    readonly_fields = ('created_by',)


@admin.register(ProductExpiry)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('product', 'datetime')
    readonly_fields = ('product',)
