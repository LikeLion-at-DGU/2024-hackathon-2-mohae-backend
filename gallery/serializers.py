# serializers.py

from rest_framework import serializers
from .models import Album, Photo, Comment, Favorite
from accounts.models import Profile
from accounts.serializers import ProfileSerializer

class AlbumSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True, default=serializers.CurrentUserDefault())

    class Meta:
        model = Album
        fields = ['id', 'user', 'name', 'created_at', 'family', 'status']

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['nickname', 'profile_picture']

class PhotoSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True, default=serializers.CurrentUserDefault())
    profile = UserProfileSerializer(source='user.profile', read_only=True)
    album = serializers.PrimaryKeyRelatedField(queryset=Album.objects.all(), allow_null=True, required=False)

    class Meta:
        model = Photo
        fields = ['id', 'user', 'profile', 'album', 'image', 'title', 'description', 'created_at', 'status', 'family']

    def create(self, validated_data):
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            user = request.user
            validated_data['user'] = user
            validated_data['family'] = user.profile.family
        return super().create(validated_data)


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True, default=serializers.CurrentUserDefault())
    profile = ProfileSerializer(source='user.profile', read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'user', 'photo', 'text', 'created_at']

class FavoriteSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True, default=serializers.CurrentUserDefault())

    class Meta:
        model = Favorite
        fields = ['id', 'user', 'photo', 'created_at']

class PhotoBookSerializer(serializers.Serializer):
    photo_ids = serializers.ListField(
        child=serializers.IntegerField(), write_only=True
    )
    pdf_url = serializers.CharField(read_only=True)
