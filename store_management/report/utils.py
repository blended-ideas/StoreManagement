from datetime import timedelta
from uuid import uuid4

import dateutil
from django.db.models import F, DecimalField
from django.db.models.aggregates import Sum
from django.db.models.functions import Coalesce


def get_expiry_report_file_path(instance, filename):
    ext = filename.split('.')[-1]
    return f"expiry_reports/{uuid4()}.{ext}"


def get_margin_report_file_path(instance, filename):
    ext = filename.split('.')[-1]
    return f"margin_reports/{uuid4()}.{ext}"


def get_sales_report_file_path(instance, filename):
    ext = filename.split('.')[-1]
    return f"sales_reports/{uuid4()}.{ext}"


def get_custom_report_queryset(date, report_type):
    from store_management.products.models import Product

    day_start = dateutil.parser.isoparse(date)
    day_end = day_start + timedelta(days=1)
    queryset = Product.objects.prefetch_related('shift_entries', 'shift_entries__shift')

    if report_type == 'DAILY':
        queryset = queryset.filter(shift_entries__shift__end_dt__range=(day_start, day_end))
    if report_type == 'WEEKLY':
        week_start = day_end - timedelta((day_end.weekday() - 6) % 7)
        week_end = week_start + timedelta(days=6)
        queryset = queryset.filter(shift_entries__shift__end_dt__range=(week_start, week_end))
    if report_type == 'MONTHLY':
        queryset = queryset.filter(shift_entries__shift__end_dt__month=day_end.month)
    if report_type == 'QUARTERLY':
        queryset = queryset.filter(shift_entries__shift__end_dt__quarter=((day_end.month - 1) // 3 + 1))

    queryset = queryset.annotate(
        sold_quantity=Coalesce(Sum(F('shift_entries__quantity')), 0),
        total_mrp=Coalesce(
            Sum(F('shift_entries__quantity') * F('shift_entries__price'), output_field=DecimalField()), 0
        ),
        margin_total=Coalesce(
            Sum(F('shift_entries__quantity') * F('shift_entries__retailer_margin'), output_field=DecimalField()), 0)
    )

    queryset = queryset.filter(sold_quantity__gt=0)
    return queryset, day_start, day_end
