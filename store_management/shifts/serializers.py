from rest_framework.relations import SlugRelatedField
from rest_framework.serializers import ModelSerializer

from .models import ShiftDetail
from ..products.serializers import ProductStockChangeSerializer


class ShiftDetailSerializer(ModelSerializer):
    entries = ProductStockChangeSerializer(many=True, required=False, read_only=True)
    user_name = SlugRelatedField(source='user', slug_field='name', required=False, read_only=True)

    class Meta:
        model = ShiftDetail
        fields = '__all__'
