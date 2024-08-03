from django_cron import CronJobBase, Schedule
from .models import Appointment
from django.utils import timezone
from datetime import timedelta
import logging

logger = logging.getLogger(__name__)

class SendAppointmentReminderCronJob(CronJobBase):
    RUN_AT_TIMES = ['03:20']  # 테스트 목적으로 03:20에 실행 (적절한 시간으로 설정)

    schedule = Schedule(run_at_times=RUN_AT_TIMES)
    code = 'health.send_appointment_reminder_cron_job'  # 고유 코드

    def do(self):
        try:
            now = timezone.now()
            tomorrow = now + timedelta(days=1)
            start_of_day = tomorrow.replace(hour=0, minute=0, second=0, microsecond=0)
            end_of_day = tomorrow.replace(hour=23, minute=59, second=59, microsecond=999999)

            appointments = Appointment.objects.filter(appointment_datetime__range=(start_of_day, end_of_day))
            logger.info(f"Found {appointments.count()} appointments for tomorrow.")

            for appointment in appointments:
                appointment.send_notification()
                logger.info(f"Notification sent for appointment {appointment.id}")

        except Exception as e:
            logger.error(f"Error in cron job: {e}", exc_info=True)
