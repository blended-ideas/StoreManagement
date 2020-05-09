# Create your views here.
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.mixins import CreateModelMixin, UpdateModelMixin, ListModelMixin, RetrieveModelMixin
from rest_framework.viewsets import GenericViewSet

from .models import Product, ProductStockChange
from .permissions import ProductPermission
from .serializers import ProductSerializer
from ..utils.common_utils import StandardResultsSetPagination


class ProductViewSet(GenericViewSet, CreateModelMixin, UpdateModelMixin, ListModelMixin, RetrieveModelMixin):
    serializer_class = ProductSerializer
    pagination_class = StandardResultsSetPagination
    queryset = Product.objects.all()
    permission_classes = [ProductPermission]
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ('name', 'category', 'barcode_entry')

    def get_queryset(self):
        return self.queryset

    def perform_create(self, serializer):
        product = serializer.save()
        ProductStockChange.objects.create(user=self.request.user, product=product, value=product.stock,
                                          changeType='INITIAL')
