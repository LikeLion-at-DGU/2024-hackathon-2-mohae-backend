from rest_framework import serializers
from .models import Calendar, FamilyInvitation

# Calendar 시리얼라이저
class CalendarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Calendar
        fields = '__all__'

class FamilyInvitationSerializer(serializers.ModelSerializer):
    class Meta:
        model = FamilyInvitation
        fields = '__all__'
