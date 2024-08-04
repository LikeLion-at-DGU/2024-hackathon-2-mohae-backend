from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MedicationViewSet, AppointmentViewSet, ChallengeViewSet, send_manual_notification

router = DefaultRouter()
router.register(r'medications', MedicationViewSet)
router.register(r'appointments', AppointmentViewSet)
router.register(r'challenges', ChallengeViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('send-notification/<int:appointment_id>/<int:patient_id>/', send_manual_notification, name='send-manual-notification'),
]
