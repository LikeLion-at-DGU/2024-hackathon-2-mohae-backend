from django.db import models
from django.contrib.auth import get_user_model
import random
import string

User = get_user_model()

def generate_family_code():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

class Family(models.Model):
    STATUS_CHOICES = [
        ('Y', 'Active'),
        ('N', 'Inactive'),
    ]

    family_id = models.AutoField(primary_key=True)
    family_name = models.CharField(max_length=255, null=False)
    family_code = models.CharField(max_length=6, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='Y')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='families')

    def save(self, *args, **kwargs):
        if not self.family_code or self.family_code == 'TEMP':
            self.family_code = self._generate_unique_family_code()
        super(Family, self).save(*args, **kwargs)
        if not self.created_by.profile.family:
            self.created_by.profile.family = self
            self.created_by.profile.save()

    def _generate_unique_family_code(self):
        code = generate_family_code()
        while Family.objects.filter(family_code=code).exists():
            code = generate_family_code()
        return code

    def __str__(self):
        return self.family_name

class BucketList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bucketlists')
    family = models.ForeignKey(Family, on_delete=models.CASCADE, related_name='bucketlists')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=1, choices=[('Y', 'Active'), ('N', 'Inactive')], default='Y')

    def __str__(self):
        return self.title
