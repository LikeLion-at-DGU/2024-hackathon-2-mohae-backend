from rest_framework import serializers
from .models import CulturalActivity, Reservation, ConfirmedReservation, Like, Category, SubCategory
from django.contrib.auth import get_user_model


User = get_user_model()

# 카테고리 직렬화기
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

# 하위 카테고리 직렬화기
class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = '__all__'

# 문화 활동 직렬화기
class CulturalActivitySerializer(serializers.ModelSerializer):
    reservation_status = serializers.SerializerMethodField()
    category = CategorySerializer(read_only=True)
    subcategory = SubCategorySerializer(read_only=True)
    thumbnail = serializers.ImageField(read_only=True)  # Ensure thumbnail is included

    class Meta:
        model = CulturalActivity
        fields = '__all__'

    def get_reservation_status(self, obj):
        confirmed_reservations_count = ConfirmedReservation.objects.filter(reservation__activity=obj).count()
        return 'Full' if confirmed_reservations_count >= obj.available_slots else 'Available'

class ReservationSerializer(serializers.ModelSerializer):
    activity = CulturalActivitySerializer(read_only=True)
    thumbnail = serializers.ImageField(read_only=True)  # Ensure thumbnail is included

    class Meta:
        model = Reservation
        fields = '__all__'
        extra_kwargs = {
            'user': {'read_only': True},
            'activity': {'queryset': CulturalActivity.objects.all()},
        }

class ConfirmedReservationSerializer(serializers.ModelSerializer):
    reservation = ReservationSerializer()
    thumbnail = serializers.ImageField(source='reservation.thumbnail', read_only=True)  # Ensure thumbnail is included

    class Meta:
        model = ConfirmedReservation
        fields = '__all__'

# 좋아요 직렬화기
class LikeSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True, default=serializers.CurrentUserDefault())

    class Meta:
        model = Like
        fields = '__all__'
