from django.db import models
from accounts.models import Profile
from users.models import Family

class Album(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='albums')
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    shared = models.BooleanField(default=False)
    family = models.ForeignKey(Family, on_delete=models.CASCADE, related_name='albums', null=True, blank=True)
    status = models.CharField(max_length=1, choices=[('Y', 'Active'), ('N', 'Inactive')], default='Y')

    def __str__(self):
        return self.name

class Photo(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='photos')
    album = models.ForeignKey(Album, on_delete=models.SET_NULL, null=True, blank=True, related_name='photos')
    image = models.ImageField(upload_to='photos/')
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=1, choices=[('Y', 'Active'), ('N', 'Inactive')], default='Y')

    def __str__(self):
        return f'{self.user.user.username} - {self.description[:20]}'

class Comment(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='comments')
    photo = models.ForeignKey(Photo, on_delete=models.CASCADE, related_name='comments', null=True, blank=True)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class Favorite(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='favorites')
    photo = models.ForeignKey(Photo, on_delete=models.CASCADE, related_name='favorites', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.user.username} - {self.photo}'
