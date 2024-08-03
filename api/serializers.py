from rest_framework import serializers
from accounts.models import Profile

class QuestionSerializer(serializers.Serializer):
    question = serializers.CharField()

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('nickname', 'profile_picture')
