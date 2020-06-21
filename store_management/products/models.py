# Create your models here.
from django.conf import settings
from django.db.models import CharField, ForeignKey, PROTECT, DecimalField, PositiveIntegerField, ImageField, \
    DateTimeField, CASCADE, BooleanField, IntegerField
from model_utils.models import UUIDModel, TimeStampedModel
from rest_framework.exceptions import ValidationError

from store_management.constants import PRODUCT_STATUS_CHANGE_CHOICES
from store_management.products.utils import get_product_upload_path


class Product(UUIDModel, TimeStampedModel):
    created_by = ForeignKey(settings.AUTH_USER_MODEL, on_delete=PROTECT)
    name = CharField(max_length=250)
    category = CharField(max_length=500, blank=True, null=True)

    landing_price = DecimalField(max_digits=9, decimal_places=2)
    price = DecimalField(max_digits=9, decimal_places=2, verbose_name='MRP')
    distributor_margin = DecimalField(max_digits=5, decimal_places=2, verbose_name='Shell Margin')
    retailer_margin = DecimalField(max_digits=5, decimal_places=2)

    stock = PositiveIntegerField()
    barcode_entry = CharField(max_length=200, unique=True)
    image = ImageField(upload_to=get_product_upload_path, blank=True, null=True)

    is_active = BooleanField(default=True)

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'

    def __str__(self):
        return self.name


class ProductExpiry(TimeStampedModel):
    user = ForeignKey(settings.AUTH_USER_MODEL, on_delete=CASCADE)
    product = ForeignKey(Product, on_delete=CASCADE)
    datetime = DateTimeField()

    class Meta:
        verbose_name = 'Product Expiry'
        verbose_name_plural = 'Products Expiry'

    def __str__(self):
        return f"{self.product} - {self.datetime}"


class ProductStockChange(TimeStampedModel):
    user = ForeignKey(settings.AUTH_USER_MODEL, on_delete=PROTECT)
    product = ForeignKey(Product, on_delete=CASCADE)
    value = IntegerField()
    changeType = CharField(choices=PRODUCT_STATUS_CHANGE_CHOICES, max_length=50)
    shift_entry = ForeignKey('shifts.ShiftEntry', on_delete=CASCADE, blank=True, null=True, related_name='entries')

    class Meta:
        verbose_name = 'Product Stock Change'
        verbose_name_plural = 'Product Stock Changes'

    def __str__(self):
        return f"{self.user} - {self.changeType} - {self.value}"

    def save(self, *args, **kwargs):
        if self.changeType == 'SHIFT' and self.shift_entry is None:
            raise ValidationError('Missing Shift Entry')
        if self.changeType == 'SHIFT_MODIFICATION' and self.shift_entry is None:
            raise ValidationError('Missing Shift Entry')
        super(ProductStockChange, self).save(*args, **kwargs)
