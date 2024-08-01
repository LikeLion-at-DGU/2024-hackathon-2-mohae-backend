from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter
from .views import AlbumViewSet, PhotoViewSet, CommentViewSet, FavoriteViewSet, PhotoBookViewSet

router = DefaultRouter()
router.register('albums', AlbumViewSet, basename='albums')
router.register('photos', PhotoViewSet, basename='photos')
router.register('comments', CommentViewSet, basename='comments')
router.register('favorites', FavoriteViewSet, basename='favorites')
router.register('photobooks', PhotoBookViewSet, basename='photobooks')

urlpatterns = [
    path('', include(router.urls)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
