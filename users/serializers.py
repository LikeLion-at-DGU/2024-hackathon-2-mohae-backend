from rest_framework import serializers
from .models import BucketList, Family
from culture.models import Like, CulturalActivity, ConfirmedReservation, Reservation
from django.contrib.auth import get_user_model
from accounts.models import Profile

User = get_user_model()

class BucketListSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True, default=serializers.CurrentUserDefault())
    family = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = BucketList
        fields = ['id', 'user', 'family', 'title', 'description', 'created_at', 'status']

class ProfileSerializer(serializers.ModelSerializer):
    family_code = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = Profile
        fields = ['user', 'phone_number', 'nickname', 'birth_date', 'address', 'profile_picture', 'family_code']

    def update(self, instance, validated_data):
        family_code = validated_data.pop('family_code', None)
        if family_code:
            if instance.family:
                raise serializers.ValidationError("You are already part of a family.")
            try:
                family = Family.objects.get(family_code=family_code)
                instance.family = family
            except Family.DoesNotExist:
                raise serializers.ValidationError("Invalid family code.")
        return super().update(instance, validated_data)

class FamilySerializer(serializers.ModelSerializer):
    profiles = ProfileSerializer(many=True, read_only=True)
    family_code = serializers.CharField(read_only=True)
    created_by = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Family
        fields = '__all__'

class CulturalActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = CulturalActivity
        fields = ['title', 'start_date', 'end_date', 'available_slots', 'price']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username']

class ReservationSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    activity = CulturalActivitySerializer()

    class Meta:
        model = Reservation
        fields = ['activity', 'user', 'reserved_at']

class ConfirmedReservationSerializer(serializers.ModelSerializer):
    reservation = ReservationSerializer()

    class Meta:
        model = ConfirmedReservation
        fields = ['reservation', 'confirmed_at']

class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ['id', 'user', 'activity', 'created_at']
