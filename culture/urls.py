from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CulturalActivityViewSet, MyReservationsViewSet

router = DefaultRouter()
router.register('activities', CulturalActivityViewSet)
router.register('my_reservations', MyReservationsViewSet, basename='my_reservations')

urlpatterns = [
    path('', include(router.urls)),
]
