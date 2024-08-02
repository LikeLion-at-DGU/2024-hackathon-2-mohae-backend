from rest_framework import serializers
from .models import BucketList, Family, FamilyInvitation
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
    class Meta:
        model = Profile
        fields = [ 'phone_number', 'nickname', 'birth_date', 'address', 'profile_picture', 'family', 'user']

class FamilySerializer(serializers.ModelSerializer):
    profiles = ProfileSerializer(many=True, read_only=True)

    class Meta:
        model = Family
        fields = '__all__'

class FamilyInvitationSerializer(serializers.ModelSerializer):
    invited_user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    invited_by = serializers.PrimaryKeyRelatedField(read_only=True, default=serializers.CurrentUserDefault())

    class Meta:
        model = FamilyInvitation
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
