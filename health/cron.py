from django_cron import CronJobBase, Schedule
from .models import Appointment
from django.utils import timezone
from datetime import timedelta

class SendAppointmentReminderCronJob(CronJobBase):
    RUN_AT_TIMES = ['02:30']  # 매일 오전 9시에 실행말고 다른걸로 테스트

    schedule = Schedule(run_at_times=RUN_AT_TIMES)
    code = 'health.send_appointment_reminder_cron_job'  # 고유 코드

    def do(self):
        now = timezone.now()
        tomorrow = now + timedelta(days=1)
        start_of_day = tomorrow.replace(hour=0, minute=0, second=0, microsecond=0)
        end_of_day = tomorrow.replace(hour=23, minute=59, second=59, microsecond=999999)

        appointments = Appointment.objects.filter(appointment_datetime__range=(start_of_day, end_of_day))

        for appointment in appointments:
            appointment.send_notification()
