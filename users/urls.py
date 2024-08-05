from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BucketListViewSet, MyPageViewSet, FamilyViewSet, ProfileViewSet, invite_family_member


app_name = 'users'

router = DefaultRouter(trailing_slash=False)
router.register('bucketlists', BucketListViewSet)
router.register('family', FamilyViewSet)
router.register('profiles', ProfileViewSet, basename='profile')

mypage_router = DefaultRouter(trailing_slash=False)
mypage_router.register('mypage', MyPageViewSet, basename='mypage')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(mypage_router.urls)),
    path('family/join/', FamilyViewSet.as_view({'post': 'join_by_code'})),
    path('invite/', invite_family_member, name='invite-family-member'),
]
