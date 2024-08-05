from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import CulturalActivity, Reservation, ConfirmedReservation, Like
from .serializers import CulturalActivitySerializer, ReservationSerializer, ConfirmedReservationSerializer, LikeSerializer
from accounts.models import Profile
from rest_framework.exceptions import NotFound

class CulturalActivityViewSet(viewsets.ModelViewSet):
    queryset = CulturalActivity.objects.filter(status='Y')
    serializer_class = CulturalActivitySerializer

class ReservationViewSet(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        activity_id = request.data.get('activity')
        subcategory_id = request.data.get('subcategory', None)
        people = request.data.get('people', 1)  # 기본값 1
        price = request.data.get('price', None)

        activity = get_object_or_404(CulturalActivity, id=activity_id)
        user = request.user

        confirmed_reservations_count = ConfirmedReservation.objects.filter(reservation__activity=activity).count()
        if confirmed_reservations_count >= activity.available_slots:
            return Response({'message': '예약 가능한 자원이 없습니다.'}, status=status.HTTP_400_BAD_REQUEST)

        reservation_data = {
            'activity': activity_id,
            'people': people,
            'price': price,
            'status': 'C'
        }
        if subcategory_id:
            reservation_data['subcategory'] = subcategory_id

        serializer = self.get_serializer(data=reservation_data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        reservation = serializer.save()

        ConfirmedReservation.objects.create(reservation=reservation)
        
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class LikeViewSet(viewsets.ModelViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        try:
            user_profile = Profile.objects.get(user=self.request.user)
        except Profile.DoesNotExist:
            raise NotFound('Profile matching query does not exist.')
        
        family = user_profile.family
        return Like.objects.filter(user__profile__family=family)

    def create(self, request, *args, **kwargs):
        activity_id = request.data.get('activity')
        activity = get_object_or_404(CulturalActivity, id=activity_id)
        user = request.user

        like, created = Like.objects.get_or_create(activity=activity, user=user)
        if not created:
            like.delete()
            return Response({'message': 'Like removed.'}, status=status.HTTP_200_OK)
        
        return Response({'message': 'Liked.'}, status=status.HTTP_201_CREATED)