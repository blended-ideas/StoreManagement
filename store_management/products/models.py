# Create your models here.
from django.conf import settings
from django.db.models import CharField, ForeignKey, PROTECT, DecimalField, PositiveIntegerField, ImageField, \
    DateTimeField, CASCADE, BooleanField, IntegerField
from model_utils.models import UUIDModel, TimeStampedModel

from store_management.constants import PRODUCT_STATUS_CHANGE_CHOICES
from store_management.products.utils import get_product_upload_path


class Product(UUIDModel):
    created_by = ForeignKey(settings.AUTH_USER_MODEL, on_delete=PROTECT)
    name = CharField(max_length=250)
    category = CharField(max_length=500, blank=True, null=True)

    price = DecimalField(max_digits=10, decimal_places=2)
    distributor_margin = DecimalField(max_digits=10, decimal_places=2)
    retailer_margin = DecimalField(max_digits=10, decimal_places=2)

    stock = PositiveIntegerField()
    barcode_entry = CharField(max_length=200)
    image = ImageField(upload_to=get_product_upload_path, blank=True, null=True)

    is_active = BooleanField(default=True)

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'


class ProductExpiry(TimeStampedModel):
    product = ForeignKey(Product, on_delete=CASCADE)
    datetime = DateTimeField()

    class Meta:
        verbose_name = 'Product Expiry'
        verbose_name_plural = 'Products Expiry'


class ProductStockChange(TimeStampedModel):
    user = ForeignKey(settings.AUTH_USER_MODEL, on_delete=PROTECT)
    product = ForeignKey(Product, on_delete=CASCADE)
    value = IntegerField()
    changeType = CharField(choices=PRODUCT_STATUS_CHANGE_CHOICES, max_length=50)

    class Meta:
        verbose_name = 'Product Stock Change'
        verbose_name_plural = 'Product Stock Changes'
