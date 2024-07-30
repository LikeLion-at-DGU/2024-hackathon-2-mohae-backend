from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save

# Profile 모델 정의
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    department = models.CharField(max_length=30, null=True, blank=True)
    hobby = models.CharField(max_length=20, null=True, blank=True)
    followings = models.ManyToManyField("self", related_name="followers", symmetrical=False)

    def __str__(self):
        return self.user.username

# User 모델이 생성될 때 Profile을 자동으로 생성하는 시그널
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

# User 모델이 저장될 때 Profile도 저장하는 시그널
@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
