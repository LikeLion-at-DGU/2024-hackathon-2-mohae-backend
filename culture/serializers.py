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

# 수정 코드
class ReservationSerializer(serializers.ModelSerializer):
    thumbnail = serializers.ImageField(allow_null=True, required=False)

    class Meta:
        model = Reservation
        fields = '__all__'
        extra_kwargs = {
            'user': {'read_only': True},
            'activity': {'queryset': CulturalActivity.objects.all()},
        }

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

# 기존 코드
# # 예약 직렬화기
# class ReservationSerializer(serializers.ModelSerializer):
#     user = serializers.PrimaryKeyRelatedField(read_only=True, default=serializers.CurrentUserDefault())
#     activity = serializers.PrimaryKeyRelatedField(queryset=CulturalActivity.objects.all())

#     class Meta:
#         model = Reservation
#         fields = '__all__'

#     def create(self, validated_data):
#         request = self.context.get('request')
#         user = request.user
#         validated_data['user'] = user
#         validated_data['start_date'] = validated_data['activity'].start_date
#         validated_data['end_date'] = validated_data['activity'].end_date
#         validated_data['thumbnail'] = validated_data['activity'].thumbnail
#         return super().create(validated_data)

# 확정된 예약 직렬화기
class ConfirmedReservationSerializer(serializers.ModelSerializer):
    reservation = ReservationSerializer()

    class Meta:
        model = ConfirmedReservation
        fields = '__all__'

        
# 좋아요 직렬화기
class LikeSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True, default=serializers.CurrentUserDefault())

    class Meta:
        model = Like
        fields = '__all__'
