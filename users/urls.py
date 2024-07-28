from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BucketListViewSet, MyPageViewSet, FamilyViewSet, FamilyInvitationViewSet

router = DefaultRouter()
router.register('bucketlists', BucketListViewSet, name='bucketlists')
router.register('family', FamilyViewSet, name='family')
router.register('invitations', FamilyInvitationViewSet, name='invitations')

mypage_router = DefaultRouter()
mypage_router.register('mypage', MyPageViewSet, name='mypage')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(mypage_router.urls)),
]