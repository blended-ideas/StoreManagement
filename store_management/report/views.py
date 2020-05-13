from datetime import timedelta

import dateutil.parser
# Create your views here.
from django.db.models import F
from django.db.models.aggregates import Sum
from django.db.models.fields import DecimalField
from django.db.models.functions import Coalesce
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from store_management.products.models import Product
from store_management.products.serializers import ProductSerializerForMargin
from store_management.shifts.models import ShiftDetail


class DailyMargin(APIView):
    def get(self, request, format=None):
        date = self.request.query_params.get('day')
        if date is None:
            return Response(data={}, status=status.HTTP_200_OK)

        day_start = dateutil.parser.isoparse(date)
        day_end = day_start + timedelta(days=1)

        margin_data = ShiftDetail.objects.filter(end_dt__range=(day_start, day_end)) \
            .aggregate(price_total=Coalesce(Sum('price_total'), 0),
                       distributor_margin_total=Coalesce(Sum('distributor_margin_total'), 0),
                       retailer_margin_total=Coalesce(Sum('retailer_margin_total'), 0))
        top_selling = Product.objects.filter(shift_entries__shift__end_dt__range=(day_start, day_end)) \
            .annotate(high_margin=Sum(F('shift_entries__retailer_margin') * F('shift_entries__quantity'),
                                      output_field=DecimalField())) \
            .annotate(high_count=Sum('shift_entries__quantity')) \
            .distinct()

        high_margin_product = top_selling.order_by('high_margin').last()
        high_count_product = top_selling.order_by('high_count').last()

        response_data = {
            'margin': margin_data,
            'high_margin_product': ProductSerializerForMargin(high_margin_product).data,
            'high_count_product': ProductSerializerForMargin(high_count_product).data
        }

        return Response(data=response_data, status=status.HTTP_200_OK)
