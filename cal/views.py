# cal/views.py
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Calendar, FamilyInvitation
from .serializers import CalendarSerializer, FamilyInvitationSerializer
from django.utils import timezone
from django.shortcuts import get_object_or_404
from rest_framework import status
from datetime import timedelta
from django.contrib.auth import get_user_model
from accounts.utils import send_kakao_message

User = get_user_model()

@api_view(['POST'])
def create_event(request):
    serializer = CalendarSerializer(data=request.data)
    if serializer.is_valid():
        event = serializer.save()
        access_token = request.user.kakao_access_token
        if access_token:
            send_kakao_message(access_token, f"새로운 일정이 추가되었습니다: {event.title}")
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def list_events(request):
    events = Calendar.objects.all()
    serializer = CalendarSerializer(events, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def event_detail(request, pk):
    event = get_object_or_404(Calendar, pk=pk)
    serializer = CalendarSerializer(event)
    return Response(serializer.data)

@api_view(['PATCH'])
def update_event(request, pk):
    event = get_object_or_404(Calendar, pk=pk)
    serializer = CalendarSerializer(event, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def delete_event(request, pk):
    event = get_object_or_404(Calendar, pk=pk)
    event.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['POST'])
def create_invitation(request):
    family_id = request.data.get('family_id')
    invited_by = request.user
    expires_at = timezone.now() + timedelta(days=7)

    invitation = FamilyInvitation.objects.create(
        family_id_id=family_id,
        invited_by=invited_by,
        expires_at=expires_at
    )

    serializer = FamilyInvitationSerializer(invitation)
    return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['POST'])
def accept_invitation(request):
    code = request.data.get('code')
    try:
        invitation = FamilyInvitation.objects.get(code=code, expires_at__gte=timezone.now())
    except FamilyInvitation.DoesNotExist:
        return Response({'error': 'Invalid or expired invitation code'}, status=status.HTTP_400_BAD_REQUEST)

    family = invitation.family
    user = request.user
    user.family = family
    user.save()

    return Response({'status': 'Invitation accepted'}, status=status.HTTP_200_OK)