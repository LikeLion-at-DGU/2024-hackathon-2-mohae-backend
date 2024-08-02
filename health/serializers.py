from rest_framework import serializers
from .models import *
from users.serializers import ProfileSerializer

class MedicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medication
        fields = '__all__'
        read_only_fields = ('user',)  # user 필드를 읽기 전용으로 설정

class AppointmentSerializer(serializers.ModelSerializer):
    patient = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = Appointment
        fields = '__all__'

class ChallengeSerializer(serializers.ModelSerializer):
    participants = serializers.StringRelatedField(many=True)

    class Meta:
        model = Challenge
        fields = '__all__'
