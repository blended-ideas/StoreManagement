from django.contrib import admin

from store_management.shifts.models import ShiftDetail, ShiftEntry


class ShiftEntryInline(admin.TabularInline):
    model = ShiftEntry
    readonly_fields = ('product', 'quantity', 'distributor_margin', 'retailer_margin', 'price')
    extra = 0


@admin.register(ShiftDetail)
class ShiftDetailAdmin(admin.ModelAdmin):
    list_display = ('user', 'status', 'end_dt')
    readonly_fields = ('user', 'price_total', 'distributor_margin_total', 'retailer_margin_total')
    inlines = [
        ShiftEntryInline
    ]
