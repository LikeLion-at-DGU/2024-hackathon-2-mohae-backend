from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CulturalActivityViewSet, MyReservationsViewSet,MyLikesViewSet

router = DefaultRouter()
router.register('activities', CulturalActivityViewSet, name= 'activities')
router.register('my_reservations', MyReservationsViewSet, name='my_reservations')
router.register('my_likes', MyLikesViewSet, name='my_likes')


urlpatterns = [
    path('', include(router.urls)),
]
