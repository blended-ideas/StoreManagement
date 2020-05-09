from django.conf import settings
from django.db.models import ForeignKey, PROTECT, DateTimeField
from model_utils.models import UUIDModel

from store_management.products.models import Product


class ShiftDetail(UUIDModel):
    user = ForeignKey(settings.AUTH_USER_MODEL, on_delete=PROTECT)
    start_dt = DateTimeField(verbose_name='Start Date/Time')
    end_dt = DateTimeField(verbose_name='End Date/Time')

    class Meta:
        verbose_name = 'Shift Detail'
        verbose_name_plural = 'Shift Details'

    def __str__(self):
        return f"{self.user} - {self.start_dt}"
