from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import ProductViewSet, ProductStockChangeViewSet, ProductExpiryViewSet

app_name = "product"

router = DefaultRouter()
router.register('product', ProductViewSet)
router.register('product_stock_change', ProductStockChangeViewSet)
router.register('product_expiry', ProductExpiryViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
