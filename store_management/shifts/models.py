from django.conf import settings
from django.db.models import ForeignKey, PROTECT, DateTimeField, CASCADE, PositiveIntegerField
from model_utils.models import UUIDModel

from store_management.products.models import Product


class ShiftDetail(UUIDModel):
    user = ForeignKey(settings.AUTH_USER_MODEL, on_delete=PROTECT)
    start_dt = DateTimeField(verbose_name='Start Date/Time')
    end_dt = DateTimeField(verbose_name='End Date/Time')

    class Meta:
        verbose_name = 'Shift Detail'
        verbose_name_plural = 'Shift Details'


class ShiftProduct(UUIDModel):
    product = ForeignKey(Product, on_delete=PROTECT)
    shift = ForeignKey(ShiftDetail, on_delete=CASCADE)
    quantity = PositiveIntegerField()

    class Meta:
        verbose_name = 'Shift Product'
        verbose_name_plural = 'Shift Products'
