from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import ShiftDetailViewSet

app_name = "shifts"

router = DefaultRouter()
router.register('detail', ShiftDetailViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
