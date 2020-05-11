from rest_framework.relations import SlugRelatedField
from rest_framework.serializers import ModelSerializer

from .models import ShiftDetail, ShiftEntry


class ShiftEntrySerializer(ModelSerializer):
    product_name = SlugRelatedField(required=False, read_only=True, slug_field='name', source='product')

    class Meta:
        model = ShiftEntry
        fields = '__all__'


class ShiftDetailSerializer(ModelSerializer):
    entries = ShiftEntrySerializer(many=True, required=False, read_only=True)
    user_name = SlugRelatedField(source='user', slug_field='name', required=False, read_only=True)

    class Meta:
        model = ShiftDetail
        fields = '__all__'
