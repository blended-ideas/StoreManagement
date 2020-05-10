from django.conf import settings
from django.db.models import ForeignKey, PROTECT, DateTimeField, F, DecimalField
from django.db.models.aggregates import Sum
from model_utils.models import UUIDModel

from store_management.products.models import Product


class ShiftDetail(UUIDModel):
    user = ForeignKey(settings.AUTH_USER_MODEL, on_delete=PROTECT)
    start_dt = DateTimeField(verbose_name='Start Date/Time')
    end_dt = DateTimeField(verbose_name='End Date/Time')

    price_total = DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    distributor_margin_total = DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    retailer_margin_total = DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    class Meta:
        verbose_name = 'Shift Detail'
        verbose_name_plural = 'Shift Details'

    def __str__(self):
        return f"{self.user} - {self.start_dt}"

    def save(self, *args, **kwargs):
        value = self.entries.all().aggregate(
            price_total=Sum(F('product__price') * F('value'), output_field=DecimalField()),
            distributor_margin_total=Sum(F('product__distributor_margin') * F('value'), output_field=DecimalField()),
            retailer_margin_total=Sum(F('product__retailer_margin') * F('value'), output_field=DecimalField()),
        )
        self.price_total = abs(value['price_total'] if value['price_total'] else 0)
        self.distributor_margin_total = abs(
            value['distributor_margin_total'] if value['distributor_margin_total'] else 0
        )
        self.retailer_margin_total = abs(value['retailer_margin_total'] if value['retailer_margin_total'] else 0)
        return super(ShiftDetail, self).save(*args, **kwargs)
