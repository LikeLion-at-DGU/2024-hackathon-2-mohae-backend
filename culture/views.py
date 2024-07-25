from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import CulturalActivity, Reservation, ConfirmedReservation
from .serializers import CulturalActivitySerializer, ReservationSerializer, ConfirmedReservationSerializer

class CulturalActivityViewSet(viewsets.ModelViewSet):
    queryset = CulturalActivity.objects.filter(status='Y')
    serializer_class = CulturalActivitySerializer

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def reserve(self, request, pk=None):
        activity = self.get_object()
        user = request.user

        # 예약 가능한 자원의 수 확인
        confirmed_reservations_count = ConfirmedReservation.objects.filter(reservation__activity=activity).count()
        if confirmed_reservations_count >= activity.available_slots:
            return Response({'message': '예약 가능한 자원이 없습니다.'}, status=status.HTTP_400_BAD_REQUEST)

        # 예약 중복 체크
        reservation = Reservation.objects.filter(activity=activity, user=user).first()
        if reservation:
            confirmed_reservation, created = ConfirmedReservation.objects.get_or_create(reservation=reservation)
            if not created:
                return Response({'message': '이미 예약된 활동입니다. 예약이 확정되었습니다.', 'status': 'C'}, status=status.HTTP_200_OK)
            return Response({'message': '예약이 확정되었습니다.', 'status': 'C'}, status=status.HTTP_201_CREATED)
        
        reservation = Reservation.objects.create(activity=activity, user=user)
        ConfirmedReservation.objects.create(reservation=reservation)
        serializer = ReservationSerializer(reservation)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class MyReservationsViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ConfirmedReservationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return ConfirmedReservation.objects.filter(reservation__user=self.request.user)
