from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import BucketList, Family
from .serializers import BucketListSerializer, FamilySerializer, LikeSerializer, CulturalActivitySerializer, ConfirmedReservationSerializer, ProfileSerializer
from culture.models import Like, ConfirmedReservation, CulturalActivity
from django.db.models import Q
from accounts.models import Profile

class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user.profile  # 로그인한 사용자의 프로필을 반환

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data)

    def perform_update(self, serializer):
        serializer.save()

class BucketListViewSet(viewsets.ModelViewSet):
    queryset = BucketList.objects.all()  # 모든 BucketList 객체를 쿼리셋으로 정의
    serializer_class = BucketListSerializer  # 이 뷰셋에서 사용할 시리얼라이저 클래스 지정
    permission_classes = [IsAuthenticated]  # 인증된 사용자만 접근 가능

    def get_queryset(self):
        user_family = self.request.user.profile.family  # 현재 요청한 사용자의 가족을 가져옴
        return self.queryset.filter(family=user_family, status='Y')  # 해당 가족의 활성화된 버킷리스트 필터링

    def perform_create(self, serializer):
        serializer.save(user=self.request.user, family=self.request.user.profile.family)  # 버킷리스트 생성 시, 사용자와 가족 정보 저장

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

class MyPageViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]  # 인증된 사용자만 접근 가능

    @action(detail=False, methods=['get'])
    def bucketlists(self, request):
        user_family = request.user.profile.family  # 현재 요청한 사용자의 가족을 가져옴
        bucketlists = BucketList.objects.filter(family=user_family, status='Y')  # 해당 가족의 활성화된 버킷리스트 필터링
        serializer = BucketListSerializer(bucketlists, many=True)  # 시리얼라이저를 사용해 데이터 직렬화
        return Response(serializer.data)  # 직렬화된 데이터를 JSON 응답으로 반환

    @action(detail=False, methods=['get'])
    def likes(self, request):
        user_family = request.user.profile.family  # 현재 요청한 사용자의 가족을 가져옴
        likes = Like.objects.filter(Q(user__family=user_family)).select_related('activity')  # 해당 가족의 좋아요 항목 필터링
        activities = CulturalActivity.objects.filter(id__in=likes.values('activity'))  # 좋아요가 눌린 활동들 필터링
        serializer = CulturalActivitySerializer(activities, many=True)  # 시리얼라이저를 사용해 데이터 직렬화
        return Response(serializer.data)  # 직렬화된 데이터를 JSON 응답으로 반환

    @action(detail=False, methods=['get'])
    def confirmed_reservations(self, request):
        user = request.user.profile  # 현재 요청한 사용자를 가져옴
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

class FamilyViewSet(viewsets.ModelViewSet):
    queryset = Family.objects.all()
    serializer_class = FamilySerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        family = serializer.save(created_by=self.request.user)
        profile = Profile.objects.get(user=self.request.user)
        profile.family = family
        profile.save()

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

    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def join_by_code(self, request):
        family_code = request.data.get('family_code')
        try:
            family = Family.objects.get(family_code=family_code)
            profile = Profile.objects.get(user=request.user)
            profile.family = family
            profile.save()
            return Response({'status': 'Family joined successfully.'})
        except Family.DoesNotExist:
            return Response({'error': 'Invalid family code.'}, status=400)

