from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BucketListViewSet, MyPageViewSet, FamilyViewSet, FamilyInvitationViewSet, ProfileViewSet

# DefaultRouter를 사용해 자동으로 URL 라우팅을 설정
router = DefaultRouter(trailing_slash=False)
router.register('bucketlists', BucketListViewSet)  # BucketListViewSet에 대한 라우트 설정
router.register('family', FamilyViewSet)  # FamilyViewSet에 대한 라우트 설정
router.register('invitations', FamilyInvitationViewSet)  # FamilyInvitationViewSet에 대한 라우트 설정
router.register('profiles', ProfileViewSet, basename='profile')  # ProfileViewSet에 대한 라우트 설정

mypage_router = DefaultRouter(trailing_slash=False)
mypage_router.register('mypage', MyPageViewSet, basename='mypage')  # MyPageViewSet에 대한 라우트 설정

urlpatterns = [
    path('', include(router.urls)),  # 라우터에 등록된 URL 포함
    path('', include(mypage_router.urls)),  # 마이페이지 라우터에 등록된 URL 포함
]
