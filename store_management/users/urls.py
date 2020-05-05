from django.urls import path, include
from rest_framework.routers import DefaultRouter

from store_management.users.views import UserViewSet

app_name = "users"

router = DefaultRouter()
router.register('user', UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
