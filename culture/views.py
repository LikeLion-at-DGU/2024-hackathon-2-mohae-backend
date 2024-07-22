from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import CulturalActivity, Reservation
from .serializers import CulturalActivitySerializer, ReservationSerializer

@api_view(['GET'])
def cultural_activities(request):
    activities = CulturalActivity.objects.filter(status='Y')
    activity_data = []
    for activity in activities:
        # 예약 상태 확인
        reservations = Reservation.objects.filter(activity=activity)
        if reservations.exists() and reservations.first().status == 'N':
            activity_dict = CulturalActivitySerializer(activity).data
            activity_dict['reservation_status'] = 'Reserved'
        else:
            activity_dict = CulturalActivitySerializer(activity).data
            activity_dict['reservation_status'] = 'Available'
        activity_data.append(activity_dict)
    return Response(activity_data, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])  # 이 엔드포인트에 접근하려면 인증이 필요
def reserve_activity(request, activity_id):
    activity = get_object_or_404(CulturalActivity, pk=activity_id, status='Y')
    user = request.user
    # 예약 중복 체크
    reservation = Reservation.objects.filter(activity=activity, user=user).first()
    if reservation:
        # 이미 예약된 경우 상태를 'N'으로 변경
        reservation.status = 'N'
        reservation.save()
        return Response({'message': '이미 예약된 활동입니다.', 'status': 'N'}, status=status.HTTP_200_OK)
    
    reservation = Reservation.objects.create(activity=activity, user=user)
    serializer = ReservationSerializer(reservation)
    return Response(serializer.data, status=status.HTTP_201_CREATED)
