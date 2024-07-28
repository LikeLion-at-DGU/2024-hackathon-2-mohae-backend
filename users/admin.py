from django.contrib import admin
from .models import Family, FamilyInvitation, BucketList 
# Register your models here.

admin.site.register(Family)
admin.site.register(FamilyInvitation)
admin.site.register(BucketList)