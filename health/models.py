import logging
from django.conf import settings
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from users.models import Family

logger = logging.getLogger(__name__)

class Medication(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    morning = models.CharField(max_length=255, blank=True, default='')
    lunch = models.CharField(max_length=255, blank=True, default='')
    dinner = models.CharField(max_length=255, blank=True, default='')
    family = models.ForeignKey(Family, on_delete=models.CASCADE, null=True, blank=True)

    def has_taken_morning_med(self):
        return self.morning.lower() == 'y'
    
    def has_taken_lunch_med(self):
        return self.lunch.lower() == 'y'

    def has_taken_dinner_med(self):
        return self.dinner.lower() == 'y'

class Appointment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='appointments')
    name = models.CharField(max_length=255)
    patient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='patient_appointments', null=True, blank=True)
    location = models.CharField(max_length=255)
    appointment_datetime = models.DateTimeField()
    family = models.ForeignKey(Family, on_delete=models.CASCADE, null=True, blank=True)

    def send_notification(self):
        from jmunja import smssend
        uid = "vini0420"
        upw = "097affdae04ad0a9357177454f4d8a"
        subject = "병원 예약 알림"
        content = (
            f"{self.patient.username}님, {self.location}에서 "
            f"{self.appointment_datetime.strftime('%Y-%m-%d %H:%M:%S')}에 예약되어 있습니다."
        )
        hpno = self.patient.profile.phone_number  # 진료자 전화번호 필요
        callback = "01083562203"

        try:
            jphone = smssend.JmunjaPhone(uid, upw)
            presult = jphone.send(subject, content, hpno)
            logger.info(f"Phone result: {presult}")

            jweb = smssend.JmunjaWeb(uid, upw)
            wresult = jweb.send(subject, content, hpno, callback)
            logger.info(f"Web result: {wresult}")

            if presult or wresult:
                logger.info(f"Notification sent for appointment {self.id}")
            else:
                logger.error(f"Failed to send notification for appointment {self.id}")

            return presult or wresult
        except Exception as e:
            logger.error(f"Error sending SMS: {e}", exc_info=True)
            return False

class Challenge(models.Model):
    title = models.CharField(max_length=255)
    start_date = models.DateField(default=timezone.now)
    end_date = models.DateField(default=timezone.now)
    participants = models.ManyToManyField(User, related_name='challenges', blank=True)
    family = models.ForeignKey(Family, on_delete=models.CASCADE, null=True, blank=True)
    image = models.ImageField(upload_to='challenges/', null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_challenges',null=True, blank=True)

    def __str__(self):
        return self.title
