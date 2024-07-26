# user/views.py

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import BucketList, Family
from .serializers import BucketListSerializer, FamilySerializer, LikeSerializer, CulturalActivitySerializer, ConfirmedReservationSerializer
from culture.models import Like, ConfirmedReservation, CulturalActivity
from django.db.models import Q

class BucketListViewSet(viewsets.ModelViewSet):
    queryset = BucketList.objects.all()
    serializer_class = BucketListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user_family = self.request.user.family
        return self.queryset.filter(family=user_family, status='Y')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user, family=self.request.user.family)


class MyPageViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['get'])
    def bucketlists(self, request):
        user_family = request.user.family
        bucketlists = BucketList.objects.filter(family=user_family, status='Y')
        serializer = BucketListSerializer(bucketlists, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def likes(self, request):
        user_family = request.user.family
        likes = Like.objects.filter(Q(user__family=user_family)).select_related('activity')
        activities = CulturalActivity.objects.filter(id__in=likes.values('activity'))
        serializer = CulturalActivitySerializer(activities, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def confirmed_reservations(self, request):
        user = request.user
        confirmed_reservations = ConfirmedReservation.objects.filter(reservation__user=user)
        serializer = ConfirmedReservationSerializer(confirmed_reservations, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def unlike(self, request, pk=None):
        try:
            like = Like.objects.get(user=request.user, activity_id=pk)
            like.delete()
            return Response({'status': 'Like removed'})
        except Like.DoesNotExist:
            return Response({'error': 'Like not found'}, status=404)


class FamilyViewSet(viewsets.ModelViewSet):
    queryset = Family.objects.all()
    serializer_class = FamilySerializer
    permission_classes = [IsAuthenticated]

    def perform_update(self, serializer):
        family = self.get_object()
        if family.created_by != self.request.user:
            raise PermissionDenied('편집 권한이 없습니다.')
        serializer.save()

    def perform_destroy(self, instance):
        family = self.get_object()
        if family.created_by != self.request.user:
            raise PermissionDenied('삭제 권한이 없습니다.')
        instance.delete()

