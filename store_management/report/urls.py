from django.urls import path, include
from rest_framework.routers import DefaultRouter

from store_management.report.views import DailyMargin, LastSevenDaySales, ExpiryReportAPI, SalesReportAPI, \
    MarginReportAPI

app_name = "report"

router = DefaultRouter()

urlpatterns = [
    path('', include(router.urls)),
    path('daily_margin/', DailyMargin.as_view(), name='daily_margin'),
    path('dashboard/sales/', LastSevenDaySales.as_view(), name='last_7day_sales'),
    path('product_expiry_report/', ExpiryReportAPI.as_view(), name='product_expiry_report'),
    path('sales_report/', SalesReportAPI.as_view(), name='sales_report'),
    path('margin_report/', MarginReportAPI.as_view(), name='margin_report'),
]
