from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CulturalActivityViewSet, MyReservationsViewSet,MyLikesViewSet

router = DefaultRouter()
router.register('activities', CulturalActivityViewSet, basename= 'activities')
router.register('my_reservations', MyReservationsViewSet, basename='my_reservations')
router.register('my_likes', MyLikesViewSet, basename='my_likes')


urlpatterns = [
    path('', include(router.urls)),
]
