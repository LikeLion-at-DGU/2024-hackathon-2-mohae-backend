from rest_framework import viewsets
from .models import Medication, Appointment, Challenge
from .serializers import MedicationSerializer, AppointmentSerializer, ChallengeSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth.models import User
from users.serializers import ProfileSerializer  # ProfileSerializer import 추가
from rest_framework import status

class MedicationViewSet(viewsets.ModelViewSet):
    queryset = Medication.objects.all()
    serializer_class = MedicationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(family=self.request.user.profile.family)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user, family=self.request.user.profile.family)

    def perform_update(self, serializer):
        serializer.save(family=self.request.user.profile.family)

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def family_members(self, request):
        family = request.user.profile.family
        if family:
            members = User.objects.filter(profile__family=family).exclude(id=request.user.id)
            serializer = ProfileSerializer(members, many=True)
            return Response(serializer.data)
        return Response([])

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

class AppointmentViewSet(viewsets.ModelViewSet):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(family=self.request.user.profile.family)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user, family=self.request.user.profile.family)

    def perform_update(self, serializer):
        serializer.save(family=self.request.user.profile.family)

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def family_members(self, request):
        family = request.user.profile.family
        if family:
            members = User.objects.filter(profile__family=family).exclude(id=request.user.id)
            serializer = ProfileSerializer(members, many=True)
            return Response(serializer.data)
        return Response([])

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

class ChallengeViewSet(viewsets.ModelViewSet):
    queryset = Challenge.objects.all()
    serializer_class = ChallengeSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(family=self.request.user.profile.family)

    def perform_create(self, serializer):
        serializer.save(family=self.request.user.profile.family)

    @action(detail=True, methods=['post'])
    def join(self, request, pk=None):
        challenge = self.get_object()
        if challenge.family != request.user.profile.family:
            return Response({'status': 'Cannot join challenges outside your family'}, status=status.HTTP_400_BAD_REQUEST)
        challenge.participants.add(request.user)
        challenge.save()
        return Response({'status': 'joined'})

    @action(detail=True, methods=['post'])
    def leave(self, request, pk=None):
        challenge = self.get_object()
        challenge.participants.remove(request.user)
        challenge.save()
        return Response({'status': 'left'})

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
