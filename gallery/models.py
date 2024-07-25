from django.db import models
from django.contrib.auth import get_user_model
from users.models import Family

User = get_user_model()

class Album(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='albums')
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    shared = models.BooleanField(default=False)
    family = models.ForeignKey(Family, on_delete=models.CASCADE, related_name='albums', null=True, blank=True)
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
    status = models.CharField(maxlength=1, choices=[('Y', 'Active'), ('N', 'Inactive')], default='Y')

    def __str__(self):
        return f'{self.user.nickname} - {self.description[:20]}'

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes')
    photo = models.ForeignKey(Photo, on_delete=models.CASCADE, related_name='likes', null=True, blank=True)
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name='likes', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'photo'), ('user', 'video')

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    photo = models.ForeignKey(Photo, on_delete=models.CASCADE, related_name='comments', null=True, blank=True)
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name='comments', null=True, blank=True)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
