# Create your views here.
from rest_framework.mixins import CreateModelMixin, ListModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.viewsets import GenericViewSet

from .models import ShiftDetail
from .permissions import ShiftDetailPermission
from .serializers import ShiftDetailSerializer
from .utils import create_shift_entries_from_data


class ShiftDetailViewSet(GenericViewSet, CreateModelMixin, ListModelMixin, RetrieveModelMixin, UpdateModelMixin):
    serializer_class = ShiftDetailSerializer
    permission_classes = [ShiftDetailPermission]
    queryset = ShiftDetail.objects.all()

    def get_queryset(self):
        queryset = self.queryset
        if self.request.user.roles.filter(label__in=['auditor', 'admin']).count() == 0:
            queryset = queryset.filter(user=self.request.user)
        return queryset

    def perform_create(self, serializer):
        entries = self.request.data.get('entries', [])
        shift_detail = serializer.save()
        create_shift_entries_from_data(shift_detail, entries)
