from django.contrib import admin

from store_management.shifts.models import ShiftDetail


@admin.register(ShiftDetail)
class ShiftDetailAdmin(admin.ModelAdmin):
    list_display = ('user', 'start_dt', 'end_dt')
    readonly_fields = ('user',)
