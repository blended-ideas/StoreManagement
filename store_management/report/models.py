from django.conf import settings
from django.db.models import FileField, ForeignKey, CASCADE, PositiveIntegerField
from django.db.models.fields import CharField, DateTimeField
from model_utils.models import TimeStampedModel, UUIDModel

from store_management.report.constants import MARGIN_REPORT_PERIOD_CHOICES
from store_management.report.utils import get_expiry_report_file_path, get_margin_report_file_path, \
    get_sales_report_file_path


class ExpiryReport(TimeStampedModel):
    user = ForeignKey(settings.AUTH_USER_MODEL, on_delete=CASCADE)
    file = FileField(upload_to=get_expiry_report_file_path)
    no_of_days = PositiveIntegerField()

    class Meta:
        verbose_name = 'Expiry Report'
        verbose_name_plural = 'Expiry Reports'

    def __str__(self):
        return f"{self.user.name} - {self.created}"


class MarginReport(TimeStampedModel, UUIDModel):
    user = ForeignKey(settings.AUTH_USER_MODEL, on_delete=CASCADE)
    file = FileField(upload_to=get_margin_report_file_path)
    period = CharField(max_length=50, choices=MARGIN_REPORT_PERIOD_CHOICES)
    start_dt = DateTimeField()
    end_dt = DateTimeField()

    class Meta:
        verbose_name = 'Margin Report'
        verbose_name_plural = 'Margin Reports'

    def __str__(self):
        return f"{self.user.name} - {self.period} - {self.created}"


class SalesReport(TimeStampedModel, UUIDModel):
    user = ForeignKey(settings.AUTH_USER_MODEL, on_delete=CASCADE)
    file = FileField(upload_to=get_sales_report_file_path)
    period = CharField(max_length=50, choices=MARGIN_REPORT_PERIOD_CHOICES)
    start_dt = DateTimeField()
    end_dt = DateTimeField()

    class Meta:
        verbose_name = 'Sales Report'
        verbose_name_plural = 'Sales Reports'

    def __str__(self):
        return f"{self.user.name} - {self.period} - {self.created}"
