from rest_framework.relations import SlugRelatedField
from rest_framework.serializers import ModelSerializer

from .models import Product, ProductStockChange


class ProductSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class ProductMinimalSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = ('name', 'category', 'price', 'distributor_margin', 'retailer_margin')


class ProductStockChangeSerializer(ModelSerializer):
    product_minimal = ProductMinimalSerializer(required=False, read_only=True, source='product')

    class Meta:
        model = ProductStockChange
        fields = '__all__'
