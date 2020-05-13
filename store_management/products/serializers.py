from rest_framework.fields import IntegerField
from rest_framework.relations import SlugRelatedField
from rest_framework.serializers import ModelSerializer

from .models import Product, ProductStockChange


class ProductSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class ProductSerializerForMargin(ModelSerializer):
    high_count = IntegerField(default=0, read_only=True, required=False)
    high_margin = IntegerField(default=0, read_only=True, required=False)

    class Meta:
        model = Product
        fields = ('id', 'name', 'category', 'price', 'distributor_margin', 'retailer_margin',
                  'high_count', 'high_margin')


class ProductMinimalSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = ('name', 'category', 'price', 'distributor_margin', 'retailer_margin')


class ProductStockChangeSerializer(ModelSerializer):
    product_minimal = ProductMinimalSerializer(required=False, read_only=True, source='product')

    class Meta:
        model = ProductStockChange
        fields = '__all__'
