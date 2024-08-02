from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import BucketList, Family, FamilyInvitation
from .serializers import BucketListSerializer, FamilySerializer, FamilyInvitationSerializer, LikeSerializer, CulturalActivitySerializer, ConfirmedReservationSerializer
from culture.models import Like, ConfirmedReservation, CulturalActivity
from django.db.models import Q
from accounts.models import User, Profile

# BucketList 모델에 대한 CRUD 작업을 처리하는 ViewSet
class BucketListViewSet(viewsets.ModelViewSet):
    queryset = BucketList.objects.all()
    serializer_class = BucketListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user_family = self.request.user.profile.family  # 현재 요청한 사용자의 가족을 가져옴
        return self.queryset.filter(family=user_family, status='Y')  # 해당 가족의 활성화된 버킷리스트 필터링

    def perform_create(self, serializer):
        serializer.save(user=self.request.user, family=self.request.user.profile.family)

    def perform_update(self, serializer):
        bucketlist = self.get_object()  # 현재 객체를 가져옴
        if bucketlist.user != self.request.user:
            raise PermissionDenied('편집 권한이 없습니다.')  # 현재 사용자가 객체의 소유자가 아닌 경우, 권한 없음 예외 발생
        serializer.save()  # 권한이 있는 경우, 업데이트 수행

    def perform_destroy(self, instance):
        bucketlist = self.get_object()  # 현재 객체를 가져옴
        if bucketlist.user != self.request.user:
            raise PermissionDenied('삭제 권한이 없습니다.')  # 현재 사용자가 객체의 소유자가 아닌 경우, 권한 없음 예외 발생
        instance.delete()  # 권한이 있는 경우, 삭제 수행

# 사용자 개인 페이지에서 다양한 정보를 제공하는 ViewSet
class MyPageViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]  # 인증된 사용자만 접근 가능

    @action(detail=False, methods=['get'])
    def bucketlists(self, request):
        user_family = request.user.profile.family
        bucketlists = BucketList.objects.filter(family=user_family, status='Y')
        serializer = BucketListSerializer(bucketlists, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def likes(self, request):
        user_family = request.user.profile.family
        likes = Like.objects.filter(Q(user__profile__family=user_family)).select_related('activity')
        activities = CulturalActivity.objects.filter(id__in=likes.values('activity'))
        serializer = CulturalActivitySerializer(activities, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def confirmed_reservations(self, request):
        user = request.user  # 현재 요청한 사용자를 가져옴
        confirmed_reservations = ConfirmedReservation.objects.filter(reservation__user=user)  # 사용자의 확정된 예약 필터링
        serializer = ConfirmedReservationSerializer(confirmed_reservations, many=True)  # 시리얼라이저를 사용해 데이터 직렬화
        return Response(serializer.data)  # 직렬화된 데이터를 JSON 응답으로 반환

    @action(detail=True, methods=['post'])
    def unlike(self, request, pk=None):
        try:
            like = Like.objects.get(user=request.user, activity_id=pk)  # 특정 활동에 대한 사용자의 좋아요 객체 가져옴
            like.delete()  # 좋아요 객체 삭제
            return Response({'status': 'Like removed'})  # 성공 메시지 반환
        except Like.DoesNotExist:
            return Response({'error': 'Like not found'}, status=404)  # 좋아요 객체가 없는 경우 오류 메시지 반환

# Family 모델에 대한 CRUD 작업 및 가족 초대와 수락 기능을 제공하는 ViewSet
class FamilyViewSet(viewsets.ModelViewSet):
    queryset = Family.objects.all()
    serializer_class = FamilySerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        family = serializer.save(created_by=self.request.user)
        profile = Profile.objects.get(user=self.request.user)
        profile.family = family
        profile.save()
        family.members.add(self.request.user)

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
            invited_user = User.objects.get(pk=request.data.get('user_id'))
            FamilyInvitation.objects.create(family=family, invited_user=invited_user, invited_by=request.user)
            return Response({'status': '초대가 발송되었습니다.'})
        except User.DoesNotExist:
            return Response({'error': '사용자를 찾을 수 없습니다.'}, status=404)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def accept_invitation(self, request, pk=None):
        try:
            invitation = FamilyInvitation.objects.get(pk=pk, invited_user=request.user)
            invitation.accepted = True
            invitation.save()
            profile = Profile.objects.get(user=request.user)
            profile.family = invitation.family
            profile.save()
            invitation.family.members.add(request.user)
            return Response({'status': '초대가 수락되었습니다.'})
        except FamilyInvitation.DoesNotExist:
            return Response({'error': '초대를 찾을 수 없습니다.'}, status=404)  # 초대 객체를 찾을 수 없는 경우 오류 메시지 반환

# FamilyInvitation 모델에 대한 CRUD 작업을 처리하는 ViewSet
class FamilyInvitationViewSet(viewsets.ModelViewSet):
    queryset = FamilyInvitation.objects.all()  # 모든 FamilyInvitation 객체를 쿼리셋으로 정의
    serializer_class = FamilyInvitationSerializer  # 이 뷰셋에서 사용할 시리얼라이저 클래스 지정
    permission_classes = [IsAuthenticated]  # 인증된 사용자만 접근 가능

    def get_queryset(self):
        return self.queryset.filter(invited_user=self.request.user)  # 현재 요청한 사용자가 초대된 가족 초대 목록 필터링

    def perform_create(self, serializer):
        serializer.save(invited_by=self.request.user)