from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CulturalActivityViewSet, MyReservationsViewSet, MyLikesViewSet, CategoryViewSet, SubCategoryViewSet

router = DefaultRouter(trailing_slash=False)
router.register('activities', CulturalActivityViewSet, basename='activities')
router.register('reservations', MyReservationsViewSet, basename='reservations')
router.register('likes', MyLikesViewSet, basename='likes')
router.register('categories', CategoryViewSet, basename='categories')
router.register('subcategories', SubCategoryViewSet, basename='subcategories')

urlpatterns = [
    path('', include(router.urls)),
]
