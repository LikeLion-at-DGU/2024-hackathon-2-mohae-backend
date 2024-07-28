from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Album(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='albums')
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    shared = models.BooleanField(default=False)
    family = models.ForeignKey('users.Family', on_delete=models.CASCADE, related_name='albums', null=True, blank=True)
    status = models.CharField(max_length=1, choices=[('Y', 'Active'), ('N', 'Inactive')], default='Y')

    def __str__(self):
        return self.name

class Photo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='photos')
    album = models.ForeignKey(Album, on_delete=models.SET_NULL, null=True, blank=True, related_name='photos')
    image = models.ImageField(upload_to='photos/')
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=1, choices=[('Y', 'Active'), ('N', 'Inactive')], default='Y')

    def __str__(self):
        return f'{self.user.nickname} - {self.description[:20]}'

class Video(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='videos')
    album = models.ForeignKey(Album, on_delete=models.SET_NULL, null=True, blank=True, related_name='videos')
    video = models.FileField(upload_to='videos/')
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=1, choices=[('Y', 'Active'), ('N', 'Inactive')], default='Y')

    def __str__(self):
        return f'{self.user.nickname} - {self.description[:20]}'

class PhotoVideoLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='photo_video_likes')
    photo = models.ForeignKey(Photo, on_delete=models.CASCADE, related_name='photo_video_likes', null=True, blank=True)
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name='photo_video_likes', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'photo'), ('user', 'video')

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    photo = models.ForeignKey(Photo, on_delete=models.CASCADE, related_name='comments', null=True, blank=True)
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name='comments', null=True, blank=True)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites')
    photo = models.ForeignKey(Photo, on_delete=models.CASCADE, related_name='favorites', null=True, blank=True)
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name='favorites', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.nickname if hasattr(self.user, "nickname") else self.user.username} - {self.photo or self.video}'
