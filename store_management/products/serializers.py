from rest_framework.serializers import ModelSerializer

from .models import Product, ProductStockChange


class ProductSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class ProductStockChangeSerializer(ModelSerializer):
    class Meta:
        model = ProductStockChange
        fields = '__all__'
