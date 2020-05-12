from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.mixins import UpdateModelMixin, ListModelMixin, RetrieveModelMixin, CreateModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ModelViewSet

from .models import UserRole
from .serializers import UserSerializer, ChangePasswordSerializer, UserRoleSerializer

User = get_user_model()


class UserViewSet(GenericViewSet, RetrieveModelMixin, ListModelMixin, UpdateModelMixin, CreateModelMixin):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()

    def get_queryset(self, *args, **kwargs):
        if self.request.user.roles.filter(label='admin').count() >= 1:
            queryset = self.queryset.filter(roles__label__in=['auditor', 'shiftworker'])
        else:
            queryset = self.queryset.filter(id=self.request.user.id)
        return queryset.distinct()

    def perform_update(self, serializer):
        user = serializer.save()
        roles = self.request.data.get('roles_change', [])
        roles_add = UserRole.objects.filter(label__in=[k for k in roles if roles[k]])
        roles_remove = UserRole.objects.filter(label__in=[k for k in roles if not roles[k]])
        user.roles.add(*roles_add)
        user.roles.remove(*roles_remove)

    def perform_create(self, serializer):
        user = serializer.save()
        password = self.request.data.get('password', [])
        user.set_password(password)
        user.save()

        roles = self.request.data.get('roles_change', [])
        roles_add = UserRole.objects.filter(label__in=[k for k in roles if roles[k]])
        roles_remove = UserRole.objects.filter(label__in=[k for k in roles if not roles[k]])
        user.roles.add(*roles_add)
        user.roles.remove(*roles_remove)

    @action(detail=False, methods=["GET"])
    def me(self, request):
        serializer = UserSerializer(request.user, context={"request": request})
        return Response(status=status.HTTP_200_OK, data=serializer.data)

    @action(detail=True, methods=['POST'])
    def change_password(self, request, *args, **kwargs):
        serializer = ChangePasswordSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        old_password = request.data.get('old_password', None)
        new_password = request.data.get('new_password', None)

        user = request.user
        if not user.check_password(old_password):
            return Response(data={'Old Password': 'Invalid Old Password'}, status=status.HTTP_400_BAD_REQUEST)
        user.set_password(new_password)
        user.save()
        return Response(data={'success': 'Password Changed'}, status=status.HTTP_200_OK)


class UserRoleViewSet(ModelViewSet):
    serializer_class = UserRoleSerializer
    queryset = UserRole.objects.all()
