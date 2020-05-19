from rest_framework.fields import IntegerField
from rest_framework.relations import SlugRelatedField
from rest_framework.serializers import ModelSerializer

from .models import Product, ProductStockChange, ProductExpiry


class ProductSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class ProductUpdateSerializer(ModelSerializer):
    stock = IntegerField(required=False, read_only=True)

    class Meta:
        model = Product
        fields = '__all__'


class ProductMinimalSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = ('name', 'category', 'price', 'distributor_margin', 'retailer_margin')


class ProductStockChangeSerializer(ModelSerializer):
    user_name = SlugRelatedField(required=False, read_only=True, slug_field='name', source='user')

    class Meta:
        model = ProductStockChange
        fields = '__all__'


class ProductExpirySerializer(ModelSerializer):
    user_name = SlugRelatedField(required=False, read_only=True, slug_field='name', source='user')
    product_name = SlugRelatedField(required=False, read_only=True, slug_field='name', source='product')

    class Meta:
        model = ProductExpiry
        fields = '__all__'
