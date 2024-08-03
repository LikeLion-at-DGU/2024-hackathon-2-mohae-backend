import django
import os
from django.utils import timezone
from health.models import Appointment

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

# 테스트용 예약 생성
appointment = Appointment.objects.create(
    user_id=1,  # 실제 존재하는 사용자 ID로 교체
    patient_id=2,  # 실제 존재하는 환자 ID로 교체
    name="Test Appointment",
    location="Test Location",
    appointment_datetime=timezone.now() + timezone.timedelta(days=1)
)

# send_notification 메서드 호출
appointment.send_notification()
print("Notification sent")
