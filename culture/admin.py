from django.contrib import admin
from .models import CulturalActivity, Reservation, ConfirmedReservation, Like
# Register your models here.

admin.site.register(CulturalActivity)
admin.site.register(Reservation)
admin.site.register(ConfirmedReservation)
admin.site.register(Like)
