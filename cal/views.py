from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Calendar
from .serializers import CalendarSerializer
from django.shortcuts import get_object_or_404
from rest_framework import status

#일정 생성
@api_view(['POST'])
def create_event(request):
    serializer = CalendarSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#일정 목록 조회
@api_view(['GET'])
def list_events(request):
    events = Calendar.objects.all()
    serializer = CalendarSerializer(events, many=True)
    return Response(serializer.data)

#일정 상세 조회
@api_view(['GET'])
def event_detail(request, pk):
    event = get_object_or_404(Calendar, pk=pk)
    serializer = CalendarSerializer(event)
    return Response(serializer.data)

#일정 수정
@api_view(['PATCH'])
def update_event(request, pk):
    event = get_object_or_404(Calendar, pk=pk)
    serializer = CalendarSerializer(event, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#일정 삭제
@api_view(['DELETE'])
def delete_event(request, pk):
    event = get_object_or_404(Calendar, pk=pk)
    event.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)
