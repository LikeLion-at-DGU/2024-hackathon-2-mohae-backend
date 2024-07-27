from rest_framework import serializers
from .models import CulturalActivity, Reservation, ConfirmedReservation, Like

class CulturalActivitySerializer(serializers.ModelSerializer):
    reservation_status = serializers.SerializerMethodField()

    class Meta:
        model = CulturalActivity
        fields = '__all__'

    def get_reservation_status(self, obj):
        confirmed_reservations_count = ConfirmedReservation.objects.filter(reservation__activity=obj).count()
        return 'Full' if confirmed_reservations_count >= obj.available_slots else 'Available'

class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = '__all__'

class ConfirmedReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConfirmedReservation
        fields = '__all__'

class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = '__all__'
