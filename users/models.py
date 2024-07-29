# users/models.py
from django.db import models
from django.conf import settings
import uuid

User = settings.AUTH_USER_MODEL

class Family(models.Model):
    STATUS_CHOICES = [
        ('Y', 'Active'),
        ('N', 'Inactive'),
    ]

    family_id = models.AutoField(primary_key=True)
    family_name = models.CharField(max_length=255, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='Y')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_families', default=1)
    members = models.ManyToManyField(User, through='FamilyMembership', related_name='families')
    invite_code = models.UUIDField(editable=False, unique=True, null=True)  # nullable로 설정
    
    def __str__(self):
        return self.family_name

class FamilyMembership(models.Model):
    family = models.ForeignKey(Family, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    joined_at = models.DateTimeField(auto_now_add=True)

class FamilyInvitation(models.Model):
    family = models.ForeignKey(Family, on_delete=models.CASCADE, related_name='invitations')
    invited_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='invitations')
    invited_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_invitations')
    created_at = models.DateTimeField(auto_now_add=True)
    accepted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.invited_user.email} invited to {self.family.family_name} by {self.invited_by.email}"

class BucketList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bucketlists')
    family = models.ForeignKey(Family, on_delete=models.CASCADE, related_name='bucketlists')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=1, choices=[('Y', 'Active'), ('N', 'Inactive')], default='Y')

    def __str__(self):
        return self.title