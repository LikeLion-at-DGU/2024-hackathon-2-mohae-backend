from rest_framework import serializers
from .models import Calendar
from users.models import Family

class CalendarSerializer(serializers.ModelSerializer):
    created_by = serializers.PrimaryKeyRelatedField(read_only=True, default=serializers.CurrentUserDefault())
    family_id = serializers.PrimaryKeyRelatedField(queryset=Family.objects.all())

    class Meta:
        model = Calendar
        fields = '__all__'
        optional_fields = ['reminder_time']
