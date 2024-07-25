from rest_framework import serializers
from .models import Album, Photo, Video, Like, Comment, Favorite

class AlbumSerializer(serializers.ModelSerializer):
    class Meta:
        model = Album
        fields = ['id', 'user', 'name', 'created_at', 'shared', 'family', 'status']

class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = ['id', 'user', 'album', 'image', 'description', 'created_at', 'status']

class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = ['id', 'user', 'album', 'video', 'description', 'created_at', 'status']

class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ['id', 'user', 'photo', 'video', 'created_at']

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'user', 'photo', 'video', 'text', 'created_at']

class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = ['id', 'user', 'photo', 'video', 'created_at']
