from datetime import timedelta

import dateutil.parser
# Create your views here.
import pytz
from django.db.models.aggregates import Sum
from django.db.models.functions import Coalesce, Trunc
from django.utils import timezone
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from store_management.report.serailizers import LastSevenDaySalesSerializer
from store_management.shifts.models import ShiftDetail


class DailyMargin(APIView):
    def get(self, request, format=None):
        date = self.request.query_params.get('day')
        if date is None:
            return Response(data={}, status=status.HTTP_200_OK)

        day_start = dateutil.parser.isoparse(date)
        day_end = day_start + timedelta(days=1)
        daily_margin = ShiftDetail.objects.filter(end_dt__range=(day_start, day_end)) \
            .aggregate(price_total=Coalesce(Sum('price_total'), 0),
                       distributor_margin_total=Coalesce(Sum('distributor_margin_total'), 0),
                       retailer_margin_total=Coalesce(Sum('retailer_margin_total'), 0))

        week_start = day_end - timedelta((day_end.weekday() - 6) % 7)
        week_end = week_start + timedelta(days=6)

        weekly_margin = ShiftDetail.objects.filter(end_dt__range=(week_start, week_end)) \
            .aggregate(price_total=Coalesce(Sum('price_total'), 0),
                       distributor_margin_total=Coalesce(Sum('distributor_margin_total'), 0),
                       retailer_margin_total=Coalesce(Sum('retailer_margin_total'), 0))

        monthly_margin = ShiftDetail.objects.filter(end_dt__month=day_end.month) \
            .aggregate(price_total=Coalesce(Sum('price_total'), 0),
                       distributor_margin_total=Coalesce(Sum('distributor_margin_total'), 0),
                       retailer_margin_total=Coalesce(Sum('retailer_margin_total'), 0))

        quarterly_margin = ShiftDetail.objects.filter(end_dt__quarter=((day_end.month - 1) // 3 + 1)) \
            .aggregate(price_total=Coalesce(Sum('price_total'), 0),
                       distributor_margin_total=Coalesce(Sum('distributor_margin_total'), 0),
                       retailer_margin_total=Coalesce(Sum('retailer_margin_total'), 0))

        response_data = {
            'daily_margin': daily_margin,
            'weekly_margin': weekly_margin,
            'monthly_margin': monthly_margin,
            'quarterly_margin': quarterly_margin
        }

        return Response(data=response_data, status=status.HTTP_200_OK)


class LastSevenDaySales(APIView):
    def get(self, request, format=None):
        last_7day = timezone.now() - timedelta(days=7)
        queryset = ShiftDetail.objects.filter(end_dt__gte=last_7day)

        queryset = queryset.annotate(sale_date=Trunc('end_dt', tzinfo=pytz.timezone('Asia/Kolkata'), kind='day'))
        queryset = queryset.values('sale_date')
        queryset = queryset.annotate(Sum("price_total"), Sum("distributor_margin_total"), Sum("retailer_margin_total"))
        queryset = queryset.order_by('sale_date')

        return Response(LastSevenDaySalesSerializer(queryset, many=True).data, status=status.HTTP_200_OK)
