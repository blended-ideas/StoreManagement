from django.contrib import admin

from store_management.shifts.models import ShiftDetail, ShiftProduct


class ShiftProductInline(admin.TabularInline):
    model = ShiftProduct
    fieldsets = (
        (None, {'fields': ('product', 'shift', 'quantity')}),
    )
    readonly_fields = ('product', 'shift', 'quantity')


@admin.register(ShiftDetail)
class ShiftDetailAdmin(admin.ModelAdmin):
    list_display = ('user', 'start_dt', 'end_dt')
    readonly_fields = ('user',)
    inlines = [
        ShiftProductInline
    ]
