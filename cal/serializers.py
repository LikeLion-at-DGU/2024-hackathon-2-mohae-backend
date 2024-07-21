from rest_framework import serializers
from .models import Calendar

# Calendar 시리얼라이저
class CalendarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Calendar
        fields = '__all__'

