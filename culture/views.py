from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import CulturalActivity, Reservation
from .serializers import CulturalActivitySerializer, ReservationSerializer


@api_view(['GET'])
@permission_classes([IsAuthenticated]) # 이 엔드포인트에 접근하려면 인증이 필요
def cultural_activities(request):
    activities = CulturalActivity.objects.filter(status='Y')
    serializer = CulturalActivitySerializer(activities, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated]) # 이 엔드포인트에 접근하려면 인증이 필요
def reserve_activity(request, activity_id):
    activity = get_object_or_404(CulturalActivity, pk=activity_id, status='Y')
    user = request.user
    reservation = Reservation.objects.create(activity=activity, user=user)
    serializer = ReservationSerializer(reservation)
    return Response(serializer.data, status=status.HTTP_201_CREATED)
