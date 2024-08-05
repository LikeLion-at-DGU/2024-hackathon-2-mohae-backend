from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BucketListViewSet, MyPageViewSet, FamilyViewSet, ProfileViewSet, invite_family_member

router = DefaultRouter(trailing_slash=False)
router.register('bucketlists', BucketListViewSet)
router.register('family', FamilyViewSet)
router.register('profiles', ProfileViewSet, basename='profiles')

mypage_router = DefaultRouter(trailing_slash=False)
mypage_router.register('mypage', MyPageViewSet, basename='mypage')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(mypage_router.urls)),
    path('family/join/', FamilyViewSet.as_view({'post': 'join_by_code'})), # 가족 코드로 가입
    path('invite/', invite_family_member, name='invite-family-member'),  # 초대 코드 발급 및 SMS 발송 엔드포인트 추가
]
