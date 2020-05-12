from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import UserViewSet, UserRoleViewSet

app_name = "users"

router = DefaultRouter()
router.register('user', UserViewSet)
router.register('roles', UserRoleViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
