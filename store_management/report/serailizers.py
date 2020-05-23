from rest_framework.serializers import Serializer, DateTimeField, DecimalField, ModelSerializer

from .models import ExpiryReport, SalesReport, MarginReport


class LastSevenDaySalesSerializer(Serializer):
    sale_date = DateTimeField(required=False, read_only=True, format="%d-%m-%Y")
    price_total__sum = DecimalField(required=False, read_only=True, decimal_places=2, max_digits=12)
    distributor_margin_total__sum = DecimalField(required=False, read_only=True, decimal_places=2, max_digits=12)
    retailer_margin_total__sum = DecimalField(required=False, read_only=True, decimal_places=2, max_digits=12)


class ExpiryReportSerializer(ModelSerializer):
    class Meta:
        model = ExpiryReport
        fields = '__all__'


class SalesReportSerializer(ModelSerializer):
    class Meta:
        model = SalesReport
        fields = '__all__'


class MarginReportSerializer(ModelSerializer):
    class Meta:
        model = MarginReport
        fields = '__all__'
