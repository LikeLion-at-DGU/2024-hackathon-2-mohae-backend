from django.db import models
from django.conf import settings
from users.models import Family

class CulturalActivity(models.Model):
    type = models.CharField(max_length=255, null=False)
    title = models.CharField(max_length=255, null=False)
    description = models.TextField(null=True, blank=True)
    date = models.DateTimeField(null=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    family = models.ForeignKey(Family, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    available_slots = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=1, choices=[('Y', 'Active'), ('N', 'Inactive')], default='Y')

    def __str__(self):
        return self.title

class Reservation(models.Model):
    activity = models.ForeignKey(CulturalActivity, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    reserved_at = models.DateTimeField(auto_now_add=True)
    STATUS_CHOICES = [
        ('P', 'Pending'),
        ('C', 'Confirmed'),
        ('N', 'Cancelled'),
    ]
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='P')

    def __str__(self):
        return f"Reservation for {self.activity.title} by {self.user.email}"

class ConfirmedReservation(models.Model):
    reservation = models.OneToOneField(Reservation, on_delete=models.CASCADE)
    confirmed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Confirmed reservation for {self.reservation.activity.title} by {self.reservation.user.email}"
