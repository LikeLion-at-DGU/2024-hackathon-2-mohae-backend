from django.db import models
from django.conf import settings
from django.utils import timezone
from users.models import Family
from django.contrib.auth.models import User

BOOL_CHOICES = [
    ('Y', 'Yes'),
    ('N', 'No'),
]

class Medication(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    morning = models.CharField(max_length=1, choices=BOOL_CHOICES, default='N')
    lunch = models.CharField(max_length=1, choices=BOOL_CHOICES, default='N')
    dinner = models.CharField(max_length=1, choices=BOOL_CHOICES, default='N')

    def has_taken_morning_med(self):
        return self.morning == 'Y'
    
    def has_taken_lunch_med(self):
        return self.lunch == 'Y'

    def has_taken_dinner_med(self):
        return self.dinner == 'Y'


class Appointment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='appointments')
    patient = models.ManyToManyField(User, related_name='patient_appointments', blank=True)
    location = models.CharField(max_length=255)
    appointment_datetime = models.DateTimeField()
    family_id = models.ForeignKey(Family, on_delete=models.CASCADE, null=True)

    def send_notification(self):
        from jmunja import smssend
        uid = "vini0420"
        upw = "097affdae04ad0a9357177454f4d8a"
        subject = "병원 예약 알림"
        content = f"Reminder: Appointment for {self.patient.all()[0].username} at {self.location} on {self.appointment_datetime.strftime('%Y-%m-%d %H:%M:%S')}"
        hpno = self.user.phone_number  # 사용자 전화번호 필요
        callback = self.user.phone_number

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
