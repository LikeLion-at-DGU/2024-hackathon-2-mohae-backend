from rest_framework import serializers
from .models import Appointment, Medication, Challenge
from django.contrib.auth.models import User

class AppointmentSerializer(serializers.ModelSerializer):
    patient = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    family = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Appointment
        fields = ['id', 'user', 'name', 'patient', 'location', 'appointment_datetime', 'family']
        read_only_fields = ('user', 'family')

class MedicationSerializer(serializers.ModelSerializer):
    family = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Medication
        fields = '__all__'
        read_only_fields = ('user', 'family')

class ChallengeSerializer(serializers.ModelSerializer):
    participants = serializers.PrimaryKeyRelatedField(many=True, queryset=User.objects.all(), required=False)
    family = serializers.PrimaryKeyRelatedField(read_only=True)
    image = serializers.ImageField(required=False)
    start_date = serializers.DateField()
    end_date = serializers.DateField()
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Challenge
        fields = '__all__'
        read_only_fields = ('family', 'user')
