from django.contrib import admin

from .models import ExpiryReport, SalesReport, MarginReport


@admin.register(ExpiryReport)
class ExpiryReportAdmin(admin.ModelAdmin):
    readonly_fields = ('user', 'file')


@admin.register(SalesReport)
class SalesReportAdmin(admin.ModelAdmin):
    readonly_fields = ('user', 'file')


@admin.register(MarginReport)
class MarginReportAdmin(admin.ModelAdmin):
    readonly_fields = ('user', 'file')
