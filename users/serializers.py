from rest_framework import serializers
from .models import Family

# Family 시리얼라이저
class FamilySerializer(serializers.ModelSerializer):
    class Meta:
        model = Family
        fields = '__all__'
