from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(CulturalActivity)
admin.site.register(Reservation)
admin.site.register(ConfirmedReservation)
admin.site.register(Like)
admin.site.register(Category)
admin.site.register(SubCategory)