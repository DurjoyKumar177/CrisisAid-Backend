from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CrisisPostViewSet

router = DefaultRouter()
router.register(r"posts", CrisisPostViewSet, basename="crisispost")

urlpatterns = [
    path("", include(router.urls)),
]