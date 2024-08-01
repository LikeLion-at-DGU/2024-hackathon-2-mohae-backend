# gallery/urls.py

from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter
from .views import AlbumViewSet, PhotoViewSet, CommentViewSet, FavoriteViewSet, PhotoBookViewSet, TagViewSet

router = DefaultRouter()
router.register('albums', AlbumViewSet, basename='albums')
router.register('photos', PhotoViewSet, basename='photos')
router.register('comments', CommentViewSet, basename='comments')
router.register('favorites', FavoriteViewSet, basename='favorites')
router.register('photobooks', PhotoBookViewSet, basename='photobooks')
router.register('tags', TagViewSet, basename='tags')

urlpatterns = [
    path('', include(router.urls)),
]

