from rest_framework import serializers
from .models import Appointment, Medication, Challenge
from django.contrib.auth.models import User

class AppointmentSerializer(serializers.ModelSerializer):
    patient = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    family = serializers.PrimaryKeyRelatedField(read_only=True)  # 읽기 전용으로 설정

    class Meta:
        model = Appointment
        fields = ['id', 'user', 'name', 'patient', 'location', 'appointment_datetime', 'family']
        read_only_fields = ('user', 'family')  # user, family 필드를 읽기 전용으로 설정

class MedicationSerializer(serializers.ModelSerializer):
    family = serializers.PrimaryKeyRelatedField(read_only=True)  # 읽기 전용으로 설정

    class Meta:
        model = Medication
        fields = '__all__'
        read_only_fields = ('user', 'family')  # user, family 필드를 읽기 전용으로 설정

class ChallengeSerializer(serializers.ModelSerializer):
    participants = serializers.StringRelatedField(many=True)
    family = serializers.PrimaryKeyRelatedField(read_only=True)  # 읽기 전용으로 설정

    class Meta:
        model = Challenge
        fields = '__all__'
        read_only_fields = ('family',)
