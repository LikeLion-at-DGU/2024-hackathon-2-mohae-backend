from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import BucketList, Family, FamilyInvitation
from .serializers import BucketListSerializer, FamilySerializer, FamilyInvitationSerializer, LikeSerializer, CulturalActivitySerializer, ConfirmedReservationSerializer
from culture.models import Like, ConfirmedReservation, CulturalActivity
from django.db.models import Q
from accounts.models import User

class BucketListViewSet(viewsets.ModelViewSet):
    queryset = BucketList.objects.all()
    serializer_class = BucketListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user_family = self.request.user.family
        return self.queryset.filter(family=user_family, status='Y')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user, family=self.request.user.family)

    def perform_update(self, serializer):
        bucketlist = self.get_object()
        if bucketlist.user != self.request.user:
            raise PermissionDenied('편집 권한이 없습니다.')
        serializer.save()

    def perform_destroy(self, instance):
        bucketlist = self.get_object()
        if bucketlist.user != self.request.user:
            raise PermissionDenied('삭제 권한이 없습니다.')
        instance.delete()

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

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

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

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def invite(self, request, pk=None):
        family = self.get_object()
        try:
            invited_user = User.objects.get(pk=request.data.get('user_id')) # 초대할 사용자를 가져옴
            FamilyInvitation.objects.create(family=family, invited_user=invited_user, invited_by=request.user) # 초대 객체 생성
            return Response({'status': '초대가 발송되었습니다.'})
        except User.DoesNotExist:
            return Response({'error': '사용자를 찾을 수 없습니다.'}, status=404)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def accept_invitation(self, request, pk=None):
        try:
            invitation = FamilyInvitation.objects.get(pk=pk, invited_user=request.user)
            invitation.accepted = True
            invitation.save() # 초대 수락 상태로 업데이트
            request.user.family = invitation.family
            request.user.save()
            return Response({'status': '초대가 수락되었습니다.'})
        except FamilyInvitation.DoesNotExist:
            return Response({'error': '초대를 찾을 수 없습니다.'}, status=404) # 초대 객체를 찾을 수 없는 경우 오류 메시지 반환

class FamilyInvitationViewSet(viewsets.ModelViewSet):
    queryset = FamilyInvitation.objects.all()
    serializer_class = FamilyInvitationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(invited_user=self.request.user)  # 현재 요청한 사용자가 초대된 가족 초대 목록 필터링

