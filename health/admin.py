from django.contrib import admin
from .models import Challenge, Appointment, Medication

@admin.register(Challenge)
class ChallengeAdmin(admin.ModelAdmin):
    list_display = ('title', 'start_date', 'end_date')
    search_fields = ('title',)
    list_filter = ('start_date', 'end_date')

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('user', 'get_patients', 'location', 'appointment_datetime', 'family_id')
    list_filter = ('appointment_datetime', 'family_id')
    search_fields = ('user__username', 'location')

    def get_patients(self, obj):
        return ", ".join([patient.username for patient in obj.patient.all()])
    get_patients.short_description = 'Patients'

@admin.register(Medication)
class MedicationAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'morning', 'lunch', 'dinner')
    list_filter = ('morning', 'lunch', 'dinner')
    search_fields = ('user__username', 'name')
