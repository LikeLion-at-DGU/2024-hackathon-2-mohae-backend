from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter
from .views import AlbumViewSet, PhotoViewSet, VideoViewSet, CommentViewSet, FavoriteViewSet

# 자동으로 URL 라우팅을 설정해주는 DefaultRouter 사용
router = DefaultRouter()
router.register('albums', AlbumViewSet, basename='albums')
router.register('photos', PhotoViewSet, basename='photos')
router.register('videos', VideoViewSet, basename='videos')
router.register('comments', CommentViewSet, basename='comments')
router.register('favorites', FavoriteViewSet, basename='favorites')

urlpatterns = [
    path('', include(router.urls)),  # 라우터에 등록된 URL 포함
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
