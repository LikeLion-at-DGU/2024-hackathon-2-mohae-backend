from django.contrib.auth.models import User
from django.db import models
from users.models import Family

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    nickname = models.CharField(max_length=30, blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    family = models.ForeignKey(Family, on_delete=models.SET_NULL, null=True, blank=True, related_name='profiles')

    def __str__(self):
        return self.user.username