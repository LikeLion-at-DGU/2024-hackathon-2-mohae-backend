from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Profile
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'

class RegisterSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(required=True)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'first_name', 'last_name', 'email', 'profile']

    def create(self, validated_data):
        profile_data = validated_data.pop('profile')
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            email=validated_data.get('email', '')
        )
        Profile.objects.create(user=user, **profile_data)
        return user

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username
        return token