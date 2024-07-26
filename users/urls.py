from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BucketListViewSet, MyPageViewSet, FamilyViewSet

router = DefaultRouter()
router.register('bucketlists', BucketListViewSet)
router.register('family', FamilyViewSet)

mypage_router = DefaultRouter()
mypage_router.register('mypage', MyPageViewSet, basename='mypage')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(mypage_router.urls)),
]
