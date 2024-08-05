from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import CulturalActivity, Reservation, ConfirmedReservation, Like
from .serializers import CulturalActivitySerializer, ReservationSerializer, ConfirmedReservationSerializer, LikeSerializer
from accounts.models import Profile

class CulturalActivityViewSet(viewsets.ModelViewSet):
    queryset = CulturalActivity.objects.filter(status='Y')
    serializer_class = CulturalActivitySerializer

class ReservationViewSet(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        activity_id = request.data.get('activity')
        subcategory_id = request.data.get('subcategory')
        people = request.data.get('people')
        price = request.data.get('price')
        
        activity = get_object_or_404(CulturalActivity, id=activity_id)
        user = request.user

        confirmed_reservations_count = ConfirmedReservation.objects.filter(reservation__activity=activity).count()
        if confirmed_reservations_count >= activity.available_slots:
            return Response({'message': '예약 가능한 자원이 없습니다.'}, status=status.HTTP_400_BAD_REQUEST)

        reservation, created = Reservation.objects.get_or_create(activity=activity, user=user)
        if not created:
            if reservation.status == 'C':
                return Response({'message': '이미 예약된 활동입니다.'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                reservation.status = 'C'
                reservation.people = people
                reservation.price = price
                reservation.subcategory_id = subcategory_id
                reservation.save()
                ConfirmedReservation.objects.create(reservation=reservation)
                serializer = self.get_serializer(reservation)
                return Response(serializer.data, status=status.HTTP_200_OK)
        
        reservation.people = people
        reservation.price = price
        reservation.subcategory_id = subcategory_id
        reservation.status = 'C'
        reservation.save()
        ConfirmedReservation.objects.create(reservation=reservation)
        serializer = self.get_serializer(reservation)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class LikeViewSet(viewsets.ModelViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # 현재 사용자의 가족이 누른 모든 좋아요를 반환
        user_profile = Profile.objects.get(user=self.request.user)
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
