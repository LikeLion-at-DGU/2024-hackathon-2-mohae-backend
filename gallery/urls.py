from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AlbumViewSet, PhotoViewSet, VideoViewSet, CommentViewSet, FavoriteViewSet

# 자동으로 URL 라우팅을 설정해주는 DefaultRouter 사용
router = DefaultRouter()
router.register('albums', AlbumViewSet, name='albums')
router.register('photos', PhotoViewSet, name='photos')
router.register('videos', VideoViewSet, name='videos')
router.register('comments', CommentViewSet, name='comments')
router.register('favorites', FavoriteViewSet, name='favorites')

urlpatterns = [
    path('', include(router.urls)),  # 라우터에 등록된 URL 포함
]
