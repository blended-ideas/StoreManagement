from django.contrib import admin

from .models import ExpiryReport


@admin.register(ExpiryReport)
class ExpiryReportAdmin(admin.ModelAdmin):
    readonly_fields = ('user', 'file')
