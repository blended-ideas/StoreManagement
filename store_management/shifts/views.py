# Create your views here.
from datetime import timedelta

import dateutil
from django.db.models import F
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.mixins import CreateModelMixin, ListModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from .models import ShiftDetail, ShiftEntry
from .permissions import ShiftDetailPermission, ShiftApprovePermission, ShiftAddProductApprovePermission, \
    ShiftEntryPermission
from .serializers import ShiftDetailSerializer, ShiftEntrySerializer
from .utils import create_shift_entries_from_data
from ..products.models import ProductStockChange
from ..utils.common_utils import StandardResultsSetPagination, get_or_none


class ShiftDetailViewSet(GenericViewSet, CreateModelMixin, ListModelMixin, RetrieveModelMixin):
    serializer_class = ShiftDetailSerializer
    permission_classes = [ShiftDetailPermission]
    pagination_class = StandardResultsSetPagination
    filter_backends = (SearchFilter, OrderingFilter)
    ordering = ['-end_dt']
    search_fields = ['user__name']
    queryset = ShiftDetail.objects.all()

    def get_queryset(self):
        queryset = self.queryset
        date = self.request.query_params.get('date', None)
        sts = self.request.query_params.get('status', None)

        if date is not None:
            day_start = dateutil.parser.isoparse(date)
            day_end = day_start + timedelta(days=1)
            queryset = queryset.filter(end_dt__range=(day_start, day_end))

        if sts is not None:
            queryset = queryset.filter(status=sts)

        if self.request.user.roles.filter(label__in=['auditor', 'admin']).count() == 0:
            queryset = queryset.filter(user=self.request.user)
        return queryset

    def perform_create(self, serializer):
        entries = self.request.data.get('entries', [])
        shift_detail = serializer.save()
        create_shift_entries_from_data(shift_detail, entries)
        shift_detail.save()

    @action(methods=['patch'], detail=True)
    def close_shift(self, request, pk=None):
        shift = self.get_object()
        if shift.status in ['WAITING_FOR_APPROVAL', 'APPROVED']:
            return Response(self.get_serializer(shift).data, status=status.HTTP_200_OK)
        shift.status = 'WAITING_FOR_APPROVAL'
        shift.save()
        return Response(self.get_serializer(shift).data, status=status.HTTP_200_OK)

    @action(methods=['patch'], detail=True, permission_classes=[ShiftApprovePermission])
    def approve(self, request, pk=None):
        shift = self.get_object()
        if shift.status == 'APPROVED':
            return Response(self.get_serializer(shift).data, status=status.HTTP_200_OK)

        shift.status = 'APPROVED'
        shift.approved_by = self.request.user
        shift.save()

        for se in shift.entries.all():
            se.product.stock = F('stock') - se.quantity
            se.product.save()

            ProductStockChange.objects.create(
                user=shift.user,
                product=se.product,
                value=-se.quantity,
                changeType='SHIFT',
                shift_entry=se
            )
        return Response(self.get_serializer(shift).data, status=status.HTTP_200_OK)

    @action(methods=['patch'], detail=True, permission_classes=[ShiftAddProductApprovePermission])
    def add_products(self, request, pk=None):
        shift = self.get_object()
        entries = self.request.data.get('entries', [])
        for entry in entries:
            se = get_or_none(ShiftEntry, shift=shift, product_id=entry['product'])
            if se is None:
                se = ShiftEntry.objects.create(shift=shift, product_id=entry['product'], quantity=0)
            se.quantity = F('quantity') + entry['quantity']
            se.distributor_margin = se.product.distributor_margin
            se.retailer_margin = se.product.retailer_margin
            se.price = se.product.price
            se.save()
        shift.save()
        return Response(self.get_serializer(shift).data, status=status.HTTP_200_OK)


class ShiftEntryViewSet(GenericViewSet, UpdateModelMixin):
    serializer_class = ShiftEntrySerializer
    permission_classes = [ShiftEntryPermission]
    pagination_class = StandardResultsSetPagination
    filter_backends = (SearchFilter, OrderingFilter)
    ordering = ['-id']
    queryset = ShiftEntry.objects.all()

    def perform_update(self, serializer):
        old_quantity_value = self.get_object().quantity
        se = serializer.save()

        quantity_change = old_quantity_value - se.quantity
        if se.shift.status == 'APPROVED':
            se.product.stock = F('stock') + quantity_change
            se.product.save()

            ProductStockChange.objects.create(
                user=self.request.user,
                product=se.product,
                value=-int(quantity_change),
                changeType='SHIFT_MODIFICATION',
                shift_entry=se
            )
        se.shift.save()
        se.refresh_from_db()
        return Response(self.get_serializer(se).data, status=status.HTTP_200_OK)
