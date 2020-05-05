# Create your models here.
from django.conf import settings
from django.db.models import CharField, ForeignKey, PROTECT, DecimalField, PositiveIntegerField, ImageField, \
    DateTimeField, CASCADE
from model_utils.models import UUIDModel, TimeStampedModel


class Product(UUIDModel):
    name = CharField(max_length=250)
    created_by = ForeignKey(settings.AUTH_USER_MODEL, on_delete=PROTECT)
    price = DecimalField(max_digits=8, decimal_places=2)
    stock = PositiveIntegerField()
    category = CharField(max_length=500)

    distributor_margin = DecimalField(max_digits=8, decimal_places=2)
    retailer_margin = DecimalField(max_digits=8, decimal_places=2)

    barcode_entry = CharField(max_length=200)
    image = ImageField(upload_to='product_images/', blank=True, null=True)

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'


class ProductExpiry(TimeStampedModel):
    product = ForeignKey(Product, on_delete=CASCADE)
    datetime = DateTimeField()

    class Meta:
        verbose_name = 'Product Expiry'
        verbose_name_plural = 'Products Expiry'
