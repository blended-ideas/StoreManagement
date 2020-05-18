from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import ProductViewSet, ProductStockChangeViewSet

app_name = "product"

router = DefaultRouter()
router.register('product', ProductViewSet)
router.register('product_stock_change', ProductStockChangeViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
