from rest_framework import viewsets
from .models import Medication, Supplement, Appointment, Challenge
from .serializers import MedicationSerializer, SupplementSerializer, AppointmentSerializer, ChallengeSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone  # 추가
from datetime import timedelta  # 추가

class MedicationViewSet(viewsets.ModelViewSet):
    queryset = Medication.objects.all()
    serializer_class = MedicationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

class SupplementViewSet(viewsets.ModelViewSet):
    queryset = Supplement.objects.all()
    serializer_class = SupplementSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

class AppointmentViewSet(viewsets.ModelViewSet):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        start_date = timezone.now()
        end_date = start_date + timedelta(days=7)
        return self.queryset.filter(user=self.request.user, appointment_datetime__range=(start_date, end_date))

class ChallengeViewSet(viewsets.ModelViewSet):
    queryset = Challenge.objects.all()
    serializer_class = ChallengeSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['post'])
    def join(self, request, pk=None):
        challenge = self.get_object()
        challenge.participants.add(request.user)
        challenge.save()
        return Response({'status': 'joined'})

    @action(detail=True, methods=['post'])
    def leave(self, request, pk=None):
        challenge = self.get_object()
        challenge.participants.remove(request.user)
        challenge.save()
        return Response({'status': 'left'})

    def get_queryset(self):
        return self.queryset.filter(participants=self.request.user)
