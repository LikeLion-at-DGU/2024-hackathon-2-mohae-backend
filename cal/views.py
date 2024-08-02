from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .models import Calendar
from .serializers import CalendarSerializer, UserSerializer
from users.models import Family
from django.shortcuts import get_object_or_404
from rest_framework import status
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated
from accounts.models import Profile
from .utils import is_user_family_member

User = get_user_model()

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_event(request):
    serializer = CalendarSerializer(data=request.data, context={'request': request})
    if serializer.is_valid():
        # 현재 사용자의 가족 ID 가져오기
        user_profile = Profile.objects.get(user=request.user)
        family = user_profile.family
        if family is None:
            return Response({"detail": "Family is not set for the user's profile."}, status=status.HTTP_400_BAD_REQUEST)

        # family_id가 유효한지 확인
        family_id = family.pk

        # 현재 사용자가 가족 구성원인지 확인
        if not is_user_family_member(request.user, family_id):
            return Response({"detail": "You are not a member of this family."}, status=status.HTTP_403_FORBIDDEN)

        event = serializer.save(created_by=request.user, family_id=family)
        
        # 참가자 목록을 가족 구성원으로 제한
        participants_ids = request.data.get('participants', [])
        participants = User.objects.filter(id__in=participants_ids, profile__family=family)
        participants = User.objects.filter(id__in=participants_ids, profile__family=family_id)
        event.participants.set(participants)  # participants 설정

        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_events(request):
    events = Calendar.objects.all()
    serializer = CalendarSerializer(events, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def event_detail(request, pk):
    event = get_object_or_404(Calendar, pk=pk)
    serializer = CalendarSerializer(event)
    return Response(serializer.data)

@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def update_event(request, pk):
    event = get_object_or_404(Calendar, pk=pk)
    serializer = CalendarSerializer(event, data=request.data, partial=True)
    if serializer.is_valid():
        participants_ids = request.data.get('participants', [])
        participants = User.objects.filter(id__in=participants_ids, profile__family=event.family_id)
        participants = User.objects.filter(id__in=participants_ids, profile__family=event.family_id)
        event.participants.set(participants)  # participants 설정

        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_event(request, pk):
    event = get_object_or_404(Calendar, pk=pk)
    event.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def family_members(request, family_id):
    family = get_object_or_404(Family, pk=family_id)
    
    # 현재 사용자가 가족 구성원인지 확인
    if not is_user_family_member(request.user, family_id):
        return Response({"detail": "You are not a member of this family."}, status=status.HTTP_403_FORBIDDEN)
    
    members = family.profile_set.all()
    members = User.objects.filter(profile__family=family)
    serializer = UserSerializer(members, many=True)
    return Response(serializer.data)
