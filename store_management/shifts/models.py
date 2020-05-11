from decimal import Decimal

from django.conf import settings
from django.db.models import ForeignKey, PROTECT, DateTimeField, F, DecimalField, PositiveIntegerField, CASCADE
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
            price_total=Sum(F('price') * F('quantity'), output_field=DecimalField()),
            distributor_margin_total=Sum(
                (F('price') * F('quantity')) * F('distributor_margin') / Decimal(100),
                output_field=DecimalField()
            ),
            retailer_margin_total=Sum(
                (F('price') * F('quantity')) * F('retailer_margin') / Decimal(100),
                output_field=DecimalField()
            ),
        )
        self.price_total = abs(value['price_total'] if value['price_total'] else 0)
        self.distributor_margin_total = abs(
            value['distributor_margin_total'] if value['distributor_margin_total'] else 0
        )
        self.retailer_margin_total = abs(value['retailer_margin_total'] if value['retailer_margin_total'] else 0)
        return super(ShiftDetail, self).save(*args, **kwargs)


class ShiftEntry(UUIDModel):
    shift = ForeignKey(ShiftDetail, on_delete=CASCADE, related_name='entries')
    product = ForeignKey(Product, on_delete=PROTECT)

    quantity = PositiveIntegerField()
    distributor_margin = DecimalField(max_digits=5, decimal_places=2, default=Decimal(0), verbose_name='Shell Margin')
    retailer_margin = DecimalField(max_digits=5, decimal_places=2, default=Decimal(0))
    price = DecimalField(max_digits=9, decimal_places=2, default=Decimal(0))

    class Meta:
        verbose_name = 'Shift Entry'
        verbose_name_plural = 'Shift Entry'

    def __str__(self):
        return f"{self.product.name} - {self.quantity}"

    def save(self, *args, **kwargs):
        print(self.pk, self.id, self.product.distributor_margin, self.product.retailer_margin, self.product.distributor_margin)
        # if self.pk is None:
        self.distributor_margin = self.product.distributor_margin
        self.retailer_margin = self.product.retailer_margin
        self.price = self.product.price
        return super(ShiftEntry, self).save(*args, **kwargs)
