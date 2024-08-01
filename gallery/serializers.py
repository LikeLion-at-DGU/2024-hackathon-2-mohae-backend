from rest_framework import serializers
from .models import Album, Photo, Comment, Favorite, Tag

class AlbumSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True, default=serializers.CurrentUserDefault())

    class Meta:
        model = Album
        fields = ['id', 'user', 'name', 'created_at', 'family', 'status']

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']

class PhotoSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True, default=serializers.CurrentUserDefault())
    tags = TagSerializer(many=True, read_only=True)
    tag_ids = serializers.PrimaryKeyRelatedField(queryset=Tag.objects.all(), write_only=True, many=True, source='tags')

    class Meta:
        model = Photo
        fields = ['id', 'user', 'album', 'image', 'title', 'description', 'tags', 'tag_ids', 'created_at', 'status']

    def create(self, validated_data):
        tags_data = validated_data.pop('tags', [])
        photo = Photo.objects.create(**validated_data)
        photo.tags.set(tags_data)
        return photo

    def update(self, instance, validated_data):
        tags_data = validated_data.pop('tags', [])
        instance = super().update(instance, validated_data)
        if tags_data:
            instance.tags.set(tags_data)
        return instance

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
