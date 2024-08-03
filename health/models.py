from django.conf import settings
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Medication(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    morning = models.CharField(max_length=255, blank=True, default='')
    lunch = models.CharField(max_length=255, blank=True, default='')
    dinner = models.CharField(max_length=255, blank=True, default='')

    def has_taken_morning_med(self):
        return self.morning.lower() == 'y'
    
    def has_taken_lunch_med(self):
        return self.lunch.lower() == 'y'

    def has_taken_dinner_med(self):
        return self.dinner.lower() == 'y'

class Appointment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='appointments')
    name = models.CharField(max_length=255)  # 예약 내용 필드 추가
    patient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='patient_appointments', null=True, blank=True)
    location = models.CharField(max_length=255)
    appointment_datetime = models.DateTimeField()

    def send_notification(self):
        from jmunja import smssend
        uid = "vini0420"
        upw = "097affdae04ad0a9357177454f4d8a"
        subject = "병원 예약 알림"
        content = f"Reminder: Appointment for {self.patient.username} at {self.location} on {self.appointment_datetime.strftime('%Y-%m-%d %H:%M:%S')}"
        hpno = self.patient.profile.phone_number  # 진료자 전화번호 필요
        callback = self.user.profile.phone_number

        jphone = smssend.JmunjaPhone(uid, upw)
        presult = jphone.send(subject, content, hpno)

        jweb = smssend.JmunjaWeb(uid, upw)
        wresult = jweb.send(subject, content, hpno, callback)

        return presult or wresult



class Challenge(models.Model):
    title = models.CharField(max_length=255)
    start_date = models.DateField(default=timezone.now)
    end_date = models.DateField(default=timezone.now)
    participants = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='challenges')

    def __str__(self):
        return self.title
