from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import ShiftDetailViewSet, ShiftEntryViewSet

app_name = "shifts"

router = DefaultRouter()
router.register('detail', ShiftDetailViewSet)
router.register('entry', ShiftEntryViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
