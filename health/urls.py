from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MedicationViewSet, AppointmentViewSet, ChallengeViewSet

router = DefaultRouter()
router.register(r'medications', MedicationViewSet)
router.register(r'appointments', AppointmentViewSet)
router.register(r'challenges', ChallengeViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
