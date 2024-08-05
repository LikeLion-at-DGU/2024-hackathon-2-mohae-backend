from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CulturalActivityViewSet, CategoryViewSet, SubCategoryViewSet, ReservationViewSet, LikeViewSet

router = DefaultRouter(trailing_slash=False)
router.register('activities', CulturalActivityViewSet, basename='activities')
router.register('categories', CategoryViewSet, basename='categories')
router.register('subcategories', SubCategoryViewSet, basename='subcategories')
router.register('reservations', ReservationViewSet, basename='reservations')
router.register('likes', LikeViewSet, basename='likes')

urlpatterns = [
    path('', include(router.urls)),
]
