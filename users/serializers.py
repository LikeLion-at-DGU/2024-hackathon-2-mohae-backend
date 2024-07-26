# user/serializers.py

from rest_framework import serializers
from .models import BucketList, Family
from culture.models import Like, CulturalActivity, ConfirmedReservation

class BucketListSerializer(serializers.ModelSerializer):
    class Meta:
        model = BucketList
        fields = ['id', 'user', 'family', 'title', 'description', 'created_at', 'status']

class FamilySerializer(serializers.ModelSerializer):
    class Meta:
        model = Family
        fields = '__all__'

class CulturalActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = CulturalActivity
        fields = '__all__'

class ConfirmedReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConfirmedReservation
        fields = '__all__'

class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ['id', 'user', 'activity', 'created_at']
