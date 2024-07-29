from rest_framework import serializers
from .models import Album, Photo, Video, PhotoVideoLike, Comment, Favorite

class AlbumSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True, default=serializers.CurrentUserDefault())

    class Meta:
        model = Album
        fields = ['id', 'user', 'name', 'created_at', 'shared', 'family', 'status']

class PhotoSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True, default=serializers.CurrentUserDefault())

    class Meta:
        model = Photo
        fields = ['id', 'user', 'album', 'image', 'description', 'created_at', 'status']

class VideoSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True, default=serializers.CurrentUserDefault())
    
    class Meta:
        model = Video
        fields = ['id', 'user', 'album', 'video', 'description', 'created_at', 'status']

class PhotoVideoLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PhotoVideoLike
        fields = ['id', 'user', 'photo', 'video', 'created_at']

class CommentSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True, default=serializers.CurrentUserDefault())

    class Meta:
        model = Comment
        fields = ['id', 'user', 'photo', 'video', 'text', 'created_at']

class FavoriteSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True, default=serializers.CurrentUserDefault())

    class Meta:
        model = Favorite
        fields = ['id', 'user', 'photo', 'video', 'created_at']
