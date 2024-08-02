from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AlbumViewSet, PhotoViewSet, CommentViewSet, FavoriteViewSet, PhotoBookViewSet

router = DefaultRouter(trailing_slash=False)
router.register('albums', AlbumViewSet, basename='albums')
router.register('photos', PhotoViewSet, basename='photos')
router.register('comments', CommentViewSet, basename='comments')
router.register('favorites', FavoriteViewSet, basename='favorites')
router.register('photobooks', PhotoBookViewSet, basename='photobooks')

urlpatterns = [
    path('', include(router.urls)),
]
