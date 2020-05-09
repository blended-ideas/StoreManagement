from rest_framework.serializers import ModelSerializer

from .models import ShiftDetail
from ..products.serializers import ProductStockChangeSerializer


class ShiftDetailSerializer(ModelSerializer):
    entries = ProductStockChangeSerializer(many=True, required=False, read_only=True)

    class Meta:
        model = ShiftDetail
        fields = '__all__'
