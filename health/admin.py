from django.contrib import admin
from .models import Appointment, Medication, Challenge

class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'patient', 'location', 'appointment_datetime')  # 'family_id' 제거
    list_filter = ('user', 'patient')  # 'family_id' 제거

class MedicationAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'name', 'morning', 'lunch', 'dinner')
    list_filter = ('user', 'name')

class ChallengeAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'start_date', 'end_date')
    list_filter = ('title',)

admin.site.register(Appointment, AppointmentAdmin)
admin.site.register(Medication, MedicationAdmin)
admin.site.register(Challenge, ChallengeAdmin)
