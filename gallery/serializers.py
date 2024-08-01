from rest_framework import serializers
from .models import Album, Photo, Comment, Favorite

class AlbumSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True, default=serializers.CurrentUserDefault())

    class Meta:
        model = Album
        fields = ['id', 'user', 'name', 'created_at', 'family', 'status']

class PhotoSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True, default=serializers.CurrentUserDefault())

    class Meta:
        model = Photo
        fields = ['id', 'user', 'album', 'image', 'title', 'description', 'created_at', 'status']

class CommentSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True, default=serializers.CurrentUserDefault())

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
