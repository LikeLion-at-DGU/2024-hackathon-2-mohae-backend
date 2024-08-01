from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import *
from .serializers import *

class CulturalActivityViewSet(viewsets.ModelViewSet):
    queryset = CulturalActivity.objects.filter(status='Y')
    serializer_class = CulturalActivitySerializer

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def reserve(self, request, pk=None):
        activity = self.get_object()
        user = request.user

        confirmed_reservations_count = Reservation.objects.filter(activity=activity, status='C').count()
        if confirmed_reservations_count >= activity.available_slots:
            return Response({'message': '예약 가능한 자원이 없습니다.'}, status=status.HTTP_400_BAD_REQUEST)

        reservation, created = Reservation.objects.get_or_create(activity=activity, user=user)
        if not created:
            if reservation.status == 'C':
                return Response({'message': '이미 예약된 활동입니다.'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                try:
                    reservation.status = 'C'
                    reservation.save()
                    ConfirmedReservation.objects.create(reservation=reservation)
                except Exception as e:
                    raise ValidationError({'message': '예약 확정 중 오류가 발생했습니다.', 'details': str(e)})
                return Response({'message': '예약이 확정되었습니다.', 'status': 'C'}, status=status.HTTP_200_OK)
        
        try:
            ConfirmedReservation.objects.create(reservation=reservation)
        except Exception as e:
            raise ValidationError({'message': '예약 확정 중 오류가 발생했습니다.', 'details': str(e)})

        reservation.status = 'C'
        reservation.save()
        serializer = ReservationSerializer(reservation)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def toggle_like(self, request, pk=None):
        activity = self.get_object()
        user = request.user

        like, created = Like.objects.get_or_create(activity=activity, user=user)
        if not created:
            like.delete()
            return Response({'message': 'Like removed.'}, status=status.HTTP_200_OK)
        
        return Response({'message': 'Liked.'}, status=status.HTTP_201_CREATED)

class MyReservationsViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ConfirmedReservationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return ConfirmedReservation.objects.filter(reservation__user=self.request.user)

class MyLikesViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = CulturalActivitySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        liked_activities = Like.objects.filter(user=user).values_list('activity', flat=True)
        return CulturalActivity.objects.filter(id__in=liked_activities)

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class SubCategoryViewSet(viewsets.ModelViewSet):
    queryset = SubCategory.objects.all()
    serializer_class = SubCategorySerializer
