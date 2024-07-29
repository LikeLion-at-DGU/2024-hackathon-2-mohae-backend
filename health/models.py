from django.db import models
from django.conf import settings
from django.utils import timezone

class Medication(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    datetime = models.DateTimeField(default=timezone.now)  # 현재 시간으로 자동 설정
    notified = models.BooleanField(default=False)

class Supplement(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    datetime = models.DateTimeField(default=timezone.now)  # 현재 시간으로 자동 설정
    notified = models.BooleanField(default=False)

class Appointment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='appointments')
    patient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='patient_appointments')
    location = models.CharField(max_length=255)
    appointment_datetime = models.DateTimeField(default=timezone.now)  # 현재 시간으로 자동 설정
    patient_image = models.ImageField(upload_to='patient_images/', null=True, blank=True)  # 프로필 이미지

class Challenge(models.Model):
    title = models.CharField(max_length=255)
    start_date = models.DateField(default=timezone.now)
    end_date = models.DateField(default=timezone.now)
    participants = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='challenges')

    def __str__(self):
        return self.title