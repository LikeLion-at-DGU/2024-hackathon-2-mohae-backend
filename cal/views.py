from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import Calendar, Family
from .serializers import CalendarSerializer
from users.serializers import FamilySerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

# 일정 생성 (Create)
@api_view(['POST'])
def create_event(request):
    if request.method == 'POST':
        serializer = CalendarSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# 일정 목록 조회 (Read)
@api_view(['GET'])
def list_events(request):
    if request.method == 'GET':
        events = Calendar.objects.all()
        serializer = CalendarSerializer(events, many=True)
        return Response(serializer.data)

# 일정 상세 조회 (Read)
@api_view(['GET'])
def event_detail(request, pk):
    try:
        event = get_object_or_404(Calendar, pk=pk)
    except Calendar.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = CalendarSerializer(event)
        return Response(serializer.data)

# 일정 수정 (Update)
@api_view(['PUT'])
def update_event(request, pk):
    try:
        event = get_object_or_404(Calendar, pk=pk)
    except Calendar.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        serializer = CalendarSerializer(event, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# 일정 삭제 (Delete)
@api_view(['DELETE'])
def delete_event(request, pk):
    try:
        event = get_object_or_404(Calendar, pk=pk)
    except Calendar.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'DELETE':
        event.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
