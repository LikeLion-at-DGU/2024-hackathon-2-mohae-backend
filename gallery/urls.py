from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AlbumViewSet, PhotoViewSet, VideoViewSet, CommentViewSet

# 자동으로 URL 라우팅을 설정해주는 DefaultRouter 사용
router = DefaultRouter()
router.register('albums', AlbumViewSet)
router.register('photos', PhotoViewSet)
router.register('videos', VideoViewSet)  # 비디오 뷰셋 추가
router.register('comments', CommentViewSet)

urlpatterns = [
    path('', include(router.urls)),  # 라우터에 등록된 URL 포함
]
