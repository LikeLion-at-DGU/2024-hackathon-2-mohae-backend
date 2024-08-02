from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Appointment
from django.utils import timezone
from datetime import timedelta

@receiver(post_save, sender=Appointment)
def schedule_appointment_notification(sender, instance, **kwargs):
    appointment_time = instance.appointment_datetime - timedelta(days=1)
    now = timezone.now()
    if now <= appointment_time:
        instance.send_notification()
