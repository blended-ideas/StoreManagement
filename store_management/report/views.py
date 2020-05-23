import os
from datetime import timedelta
from uuid import uuid4

import dateutil.parser
# Create your views here.
import pytz
import xlsxwriter
from django.core.files import File
from django.db.models import F, ExpressionWrapper
from django.db.models.aggregates import Sum
from django.db.models.fields import DurationField, DecimalField
from django.db.models.functions import Coalesce, Trunc
from django.utils import timezone
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from store_management.products.models import ProductExpiry
from store_management.shifts.models import ShiftDetail
from .models import ExpiryReport, SalesReport, MarginReport
from .serailizers import LastSevenDaySalesSerializer, ExpiryReportSerializer, SalesReportSerializer, \
    MarginReportSerializer
from .utils import get_custom_report_queryset


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


class ExpiryReportAPI(APIView):
    def post(self, request, format=None):
        days = request.data.get('days', 10)
        today = timezone.now()
        end_dt = today + timedelta(days=days)
        queryset = ProductExpiry.objects.filter(datetime__range=(today, end_dt))
        queryset = queryset.order_by('datetime') \
            .select_related('product') \
            .annotate(diff_days=ExpressionWrapper(F('datetime') - today, output_field=DurationField()),
                      total_value=ExpressionWrapper(F('product__stock') * F('product__price'),
                                                    output_field=DecimalField()))

        if not os.path.exists('temp_files'):
            os.makedirs('temp_files')

        file_name = f'temp_files/{uuid4()}.xlsx'
        workbook = xlsxwriter.Workbook(file_name)
        worksheet = workbook.add_worksheet()

        headers = ['Sl.no', 'Product', 'MRP', 'Quantity', 'Total MRP Value', 'Expiry Day', 'No of Days for Expiry']
        row = 0
        col = 0
        for header in headers:
            worksheet.write(row, col, header)
            col = col + 1

        values = queryset.values('product__name', 'product__price', 'product__stock', 'datetime', 'diff_days',
                                 'total_value')
        row = 1
        col = 0
        for entry in values:
            worksheet.write(row, col, row)
            worksheet.write(row, col + 1, entry['product__name'])
            worksheet.write(row, col + 2, entry['product__price'])
            worksheet.write(row, col + 3, entry['product__stock'])
            worksheet.write(row, col + 4, entry['total_value'])
            worksheet.write(row, col + 5, entry['datetime'].strftime('%d/%m/%y'))
            worksheet.write(row, col + 6, entry['diff_days'].days)
            row += 1
        workbook.close()
        with open(file_name, 'rb') as fi:
            fl = File(fi, name=os.path.basename(fi.name))
            report = ExpiryReport.objects.create(user=self.request.user, file=fl, no_of_days=days)
            try:
                os.remove(file_name)
            except OSError:
                pass
        return Response(data=ExpiryReportSerializer(report, context={'request': self.request}).data,
                        status=status.HTTP_201_CREATED)


class SalesReportAPI(APIView):
    def post(self, request, format=None):
        date = request.data.get('date', None)
        report_type = request.data.get('report_type', None)

        if date is None:
            return Response({'date': 'Missing/Invalid Date'}, status=status.HTTP_400_BAD_REQUEST)
        if report_type not in ['DAILY', 'WEEKLY', 'MONTHLY', 'QUARTERLY']:
            return Response({'report_period': 'Missing/Invalid Report Period'}, status=status.HTTP_400_BAD_REQUEST)

        queryset, start_dt, end_dt = get_custom_report_queryset(date, report_type)

        if not os.path.exists('temp_files'):
            os.makedirs('temp_files')

        file_name = f'temp_files/{uuid4()}.xlsx'
        workbook = xlsxwriter.Workbook(file_name)
        worksheet = workbook.add_worksheet()

        headers = ['Sl.no', 'Product', 'MRP', 'Quantity', 'Total MRP Value']
        row = 0
        col = 0
        for header in headers:
            worksheet.write(row, col, header)
            col = col + 1

        values = queryset.values('name', 'price', 'sold_quantity', 'total_mrp')
        row = 1
        col = 0
        for entry in values:
            worksheet.write(row, col, row)
            worksheet.write(row, col + 1, entry['name'])
            worksheet.write(row, col + 2, entry['price'])
            worksheet.write(row, col + 3, entry['sold_quantity'])
            worksheet.write(row, col + 4, entry['total_mrp'])
            row += 1
        workbook.close()
        with open(file_name, 'rb') as fi:
            fl = File(fi, name=os.path.basename(fi.name))
            report = SalesReport.objects.create(user=self.request.user, file=fl, period=report_type,
                                                start_dt=start_dt, end_dt=end_dt)
            try:
                os.remove(file_name)
            except OSError:
                pass

        return Response(data=SalesReportSerializer(report, context={'request': self.request}).data,
                        status=status.HTTP_201_CREATED)


class MarginReportAPI(APIView):
    def post(self, request, format=None):
        date = request.data.get('date', None)
        report_type = request.data.get('report_type', None)

        if date is None:
            return Response({'date': 'Missing/Invalid Date'}, status=status.HTTP_400_BAD_REQUEST)
        if report_type not in ['DAILY', 'WEEKLY', 'MONTHLY', 'QUARTERLY']:
            return Response({'report_period': 'Missing/Invalid Report Period'}, status=status.HTTP_400_BAD_REQUEST)

        queryset, start_dt, end_dt = get_custom_report_queryset(date, report_type)

        if not os.path.exists('temp_files'):
            os.makedirs('temp_files')

        file_name = f'temp_files/{uuid4()}.xlsx'
        workbook = xlsxwriter.Workbook(file_name)
        worksheet = workbook.add_worksheet()

        headers = ['Sl.no', 'Product', 'MRP', 'Quantity', 'Total MRP Value', 'Margin %', 'Margin Total']
        row = 0
        col = 0
        for header in headers:
            worksheet.write(row, col, header)
            col = col + 1

        print(queryset.values('name', 'margin_total'))
        values = queryset.values('name', 'price', 'sold_quantity', 'total_mrp', 'retailer_margin', 'margin_total')
        row = 1
        col = 0
        for entry in values:
            worksheet.write(row, col, row)
            worksheet.write(row, col + 1, entry['name'])
            worksheet.write(row, col + 2, entry['price'])
            worksheet.write(row, col + 3, entry['sold_quantity'])
            worksheet.write(row, col + 4, entry['total_mrp'])
            worksheet.write(row, col + 5, entry['retailer_margin'])
            worksheet.write(row, col + 6, entry['margin_total'])
            row += 1
        workbook.close()
        with open(file_name, 'rb') as fi:
            fl = File(fi, name=os.path.basename(fi.name))
            report = MarginReport.objects.create(user=self.request.user, file=fl, period=report_type,
                                                 start_dt=start_dt, end_dt=end_dt)
            try:
                os.remove(file_name)
            except OSError:
                pass

        return Response(data=MarginReportSerializer(report, context={'request': self.request}).data,
                        status=status.HTTP_201_CREATED)
