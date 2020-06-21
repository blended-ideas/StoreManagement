# Create your views here.

from django.db.models import F
from django.utils import timezone
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.mixins import CreateModelMixin, UpdateModelMixin, ListModelMixin, RetrieveModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from .models import Product, ProductStockChange, ProductExpiry
from .permissions import ProductPermission, ProductExpiryPermission, StockChangePermissions
from .serializers import ProductSerializer, ProductUpdateSerializer, ProductStockChangeSerializer, \
    ProductExpirySerializer
from ..utils.common_utils import StandardResultsSetPagination


class ProductViewSet(GenericViewSet, CreateModelMixin, UpdateModelMixin, ListModelMixin, RetrieveModelMixin):
    serializer_class = ProductSerializer
    pagination_class = StandardResultsSetPagination
    queryset = Product.objects.all()
    permission_classes = [ProductPermission]
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ('name', 'category', 'barcode_entry')
    ordering = ['name']

    def get_serializer_class(self):
        if self.request.method == 'PATCH':
            return ProductUpdateSerializer
        return ProductSerializer

    def get_queryset(self):
        return self.queryset

    def perform_create(self, serializer):
        product = serializer.save()
        ProductStockChange.objects.create(user=self.request.user, product=product, value=product.stock,
                                          changeType='INITIAL_STOCK')

    @action(methods=['POST'], detail=True, permission_classes=[StockChangePermissions])
    def add_stock(self, request, pk=None):
        change_value = request.data.get('changeValue', None)
        if change_value is None:
            return Response({'change_value': 'Missing Value to be Added'}, status=status.HTTP_400_BAD_REQUEST)
        product = self.get_object()

        product.stock = F('stock') + change_value
        product.save()
        psc = ProductStockChange.objects.create(
            user=self.request.user,
            product=product,
            value=change_value,
            changeType='ADDITION',
        )

        product.refresh_from_db()
        return Response({
            'psc': ProductStockChangeSerializer(psc).data,
            'new_value': product.stock
        }, status=status.HTTP_200_OK)

    @action(methods=['POST'], detail=True, permission_classes=[StockChangePermissions])
    def reduce_stock(self, request, pk=None):
        change_value = request.data.get('changeValue', None)
        if change_value is None:
            return Response({'change_value': 'Missing Value to be Added'}, status=status.HTTP_400_BAD_REQUEST)
        product = self.get_object()

        if (product.stock - change_value) < 0:
            return Response({'change_value': 'Reduction value cannot be less than available stock'},
                            status=status.HTTP_400_BAD_REQUEST)

        product.stock = F('stock') - change_value
        product.save()
        psc = ProductStockChange.objects.create(
            user=self.request.user,
            product=product,
            value=change_value,
            changeType='DEDUCTION',
        )

        product.refresh_from_db()
        return Response({
            'psc': ProductStockChangeSerializer(psc).data,
            'new_value': product.stock
        }, status=status.HTTP_200_OK)

    @action(methods=['POST'], detail=True, permission_classes=[StockChangePermissions])
    def modify_image(self, request, pk=None):
        product = self.get_object()
        if 'file' in self.request.FILES:
            product.image = self.request.FILES['file']
        serializer = self.get_serializer(product)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class ProductStockChangeViewSet(GenericViewSet, ListModelMixin, RetrieveModelMixin):
    serializer_class = ProductStockChangeSerializer
    pagination_class = StandardResultsSetPagination
    queryset = ProductStockChange.objects.all()
    permission_classes = [IsAuthenticated]
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ('product__name', 'product__category', 'product__barcode_entry')
    ordering = ['-created']

    def get_queryset(self):
        queryset = self.queryset
        product = self.request.query_params.get('product', None)

        if product is not None:
            queryset = queryset.filter(product=product)
        return queryset


class ProductExpiryViewSet(GenericViewSet, ListModelMixin, RetrieveModelMixin, CreateModelMixin):
    serializer_class = ProductExpirySerializer
    pagination_class = StandardResultsSetPagination
    queryset = ProductExpiry.objects.all()
    permission_classes = [ProductExpiryPermission]
    filter_backends = (SearchFilter, OrderingFilter)
    ordering = ['datetime']

    def get_queryset(self):
        queryset = self.queryset
        product = self.request.query_params.get('product', None)
        after_today = self.request.query_params.get('after_today', None)

        if product is not None:
            queryset = queryset.filter(product=product)
        if after_today is not None and after_today == 'true':
            queryset = queryset.filter(datetime__gte=timezone.now())
        return queryset
