from rest_framework import serializers
from .models import Calendar
from django.contrib.auth import get_user_model
from users.models import Family

User = get_user_model()

class CalendarSerializer(serializers.ModelSerializer):
    created_by = serializers.PrimaryKeyRelatedField(read_only=True, default=serializers.CurrentUserDefault())
    family_id = serializers.PrimaryKeyRelatedField(queryset=Family.objects.all())
    participants = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), many=True)

    class Meta:
        model = Calendar
        fields = ['event_id', 'title', 'start', 'end', 'participants', 'emoji', 'emoji_text', 'created_by', 'family_id', 'created_at', 'updated_at', 'status']
