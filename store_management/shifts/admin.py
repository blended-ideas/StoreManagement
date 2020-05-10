from django.contrib import admin

from store_management.shifts.models import ShiftDetail


@admin.register(ShiftDetail)
class ShiftDetailAdmin(admin.ModelAdmin):
    list_display = ('user', 'end_dt')
    readonly_fields = ('user', 'price_total', 'distributor_margin_total', 'retailer_margin_total')
