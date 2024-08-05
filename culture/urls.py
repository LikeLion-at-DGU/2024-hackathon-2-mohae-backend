from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CulturalActivityViewSet, ReservationViewSet, LikeViewSet


app_name = 'culture'

router = DefaultRouter(trailing_slash=False)
router.register('activities', CulturalActivityViewSet, basename='activities')
router.register('reservations', ReservationViewSet, basename='reservations')
router.register('likes', LikeViewSet, basename='likes')

urlpatterns = [
    path('', include(router.urls)),
]
