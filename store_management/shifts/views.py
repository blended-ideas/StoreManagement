# Create your views here.
from datetime import timedelta, datetime

import dateutil
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.mixins import CreateModelMixin, ListModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.viewsets import GenericViewSet

from .models import ShiftDetail
from .permissions import ShiftDetailPermission
from .serializers import ShiftDetailSerializer
from .utils import create_shift_entries_from_data
from ..utils.common_utils import StandardResultsSetPagination


class ShiftDetailViewSet(GenericViewSet, CreateModelMixin, ListModelMixin, RetrieveModelMixin, UpdateModelMixin):
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

        if date is not None:
            day_start = dateutil.parser.isoparse(date)
            day_end = day_start + timedelta(days=1)
            queryset = queryset.filter(end_dt__range=(day_start, day_end))

        if self.request.user.roles.filter(label__in=['auditor', 'admin']).count() == 0:
            queryset = queryset.filter(user=self.request.user)
        return queryset

    def perform_create(self, serializer):
        entries = self.request.data.get('entries', [])
        shift_detail = serializer.save()
        create_shift_entries_from_data(shift_detail, entries)
        shift_detail.save()
