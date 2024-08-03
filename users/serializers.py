from rest_framework import serializers
from .models import BucketList, Family
from culture.models import Like, CulturalActivity, ConfirmedReservation
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
        fields = ['phone_number', 'nickname', 'birth_date', 'address', 'profile_picture', 'family_code']

    def update(self, instance, validated_data):
        family_code = validated_data.pop('family_code', None)
        if family_code:
            try:
                family = Family.objects.get(family_code=family_code)
                instance.family = family
            except Family.DoesNotExist:
                raise serializers.ValidationError("Invalid family code.")
        return super().update(instance, validated_data)

class FamilySerializer(serializers.ModelSerializer):
    profiles = ProfileSerializer(many=True, read_only=True)
    family_code = serializers.CharField(read_only=True)  # 읽기 전용으로 설정
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
