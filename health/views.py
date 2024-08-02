from rest_framework import viewsets
from .models import Medication, Appointment, Challenge
from .serializers import MedicationSerializer, AppointmentSerializer, ChallengeSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from users.models import Family
from django.contrib.auth.models import User

class MedicationViewSet(viewsets.ModelViewSet):
    queryset = Medication.objects.all()
    serializer_class = MedicationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # 로그인한 사용자와 관련된 데이터만 반환
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        # 생성 시 로그인한 사용자를 자동으로 설정
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        # 업데이트 시 로그인한 사용자를 자동으로 설정
        serializer.save(user=self.request.user)


class AppointmentViewSet(viewsets.ModelViewSet):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def family_members(self, request):
        family = request.user.profile.family
        if family:
            members = User.objects.filter(profile__family=family).exclude(id=request.user.id)
            serializer = ProfileSerializer(members, many=True)
            return Response(serializer.data)
        return Response([])

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
