from rest_framework import serializers
from .models import Calendar
from users.models import Family
from django.contrib.auth.models import User

class CalendarSerializer(serializers.ModelSerializer):
    created_by = serializers.PrimaryKeyRelatedField(read_only=True, default=serializers.CurrentUserDefault())
    family_id = serializers.PrimaryKeyRelatedField(queryset=Family.objects.all())
    participants = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), many=True)

    class Meta:
        model = Calendar
        fields = '__all__'


