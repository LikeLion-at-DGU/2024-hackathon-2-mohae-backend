from rest_framework import serializers
from .models import CulturalActivity, Reservation

class CulturalActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = CulturalActivity
        fields = '__all__'

class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = '__all__'
