from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BucketListViewSet, MyPageViewSet, FamilyViewSet, FamilyInvitationViewSet

router = DefaultRouter()
router.register('bucketlists', BucketListViewSet, basename='bucketlists')
router.register('family', FamilyViewSet, basename='family')
router.register('invitations', FamilyInvitationViewSet, basename='invitations')
router.register('mypage', MyPageViewSet, basename='mypage')

urlpatterns = [
    path('', include(router.urls)),
]
