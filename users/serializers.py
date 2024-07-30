from rest_framework import serializers
from .models import BucketList, Family, FamilyInvitation
from culture.models import Like, CulturalActivity, ConfirmedReservation
from django.contrib.auth import get_user_model


User = get_user_model()
class BucketListSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True, default=serializers.CurrentUserDefault())

    class Meta:
        model = BucketList
        fields = ['id', 'user', 'family', 'title', 'description', 'created_at', 'status']

class FamilySerializer(serializers.ModelSerializer):
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
