from django.conf import settings
from django.db.models import FileField, ForeignKey, CASCADE, PositiveIntegerField
from model_utils.models import TimeStampedModel

from store_management.report.utils import get_expiry_report_file_path


class ExpiryReport(TimeStampedModel):
    user = ForeignKey(settings.AUTH_USER_MODEL, on_delete=CASCADE)
    file = FileField(upload_to=get_expiry_report_file_path)
    no_of_days = PositiveIntegerField()

    class Meta:
        verbose_name = 'Expiry Report'
        verbose_name_plural = 'Expiry Reports'

    def __str__(self):
        return f"{self.user.name} - {self.created}"
