from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework.decorators import action, api_view, permission_classes
from .models import BucketList, Family
from .serializers import BucketListSerializer, FamilySerializer, LikeSerializer, CulturalActivitySerializer, ConfirmedReservationSerializer, ProfileSerializer
from culture.models import Like, ConfirmedReservation, CulturalActivity
from django.db.models import Q
from accounts.models import Profile
from sms.sms_service import send_sms  # 추가
from django.http import JsonResponse # 추강
import logging
import random

logger = logging.getLogger(__name__)

class ProfileViewSet(viewsets.ModelViewSet):
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Profile.objects.filter(user=self.request.user)
    
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
        serializer.save(user=self.request.user)  # 현재 로그인된 사용자의 user 값을 자동으로 할당


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
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['get'])
    def bucketlists(self, request):
        user_family = request.user.profile.family
        if not user_family:
            return Response({'error': 'No family found'}, status=404)
        bucketlists = BucketList.objects.filter(family=user_family, status='Y')
        serializer = BucketListSerializer(bucketlists, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def likes(self, request):
        user_family = request.user.profile.family
        if not user_family:
            return Response({'error': 'No family found'}, status=404)
        likes = Like.objects.filter(user__profile__family=user_family).select_related('activity')
        activities = CulturalActivity.objects.filter(id__in=likes.values('activity'))
        serializer = CulturalActivitySerializer(activities, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def confirmed_reservations(self, request):
        user_family = request.user.profile.family
        if not user_family:
            return Response({'error': 'No family found'}, status=404)
        confirmed_reservations = ConfirmedReservation.objects.filter(
            reservation__user__profile__family=user_family
        ).order_by('-confirmed_at')  # 가족의 확정된 예약을 확정된 시간 기준으로 내림차순 정렬
        serializer = ConfirmedReservationSerializer(confirmed_reservations, many=True)  # 시리얼라이저를 사용해 데이터 직렬화
        return Response(serializer.data)  # 직렬화된 데이터를 JSON 응답으로 반환

    @action(detail=True, methods=['post'])
    def unlike(self, request, pk=None):
        try:
            like = Like.objects.get(user=request.user, activity_id=pk)
            like.delete()
            return Response({'status': 'Like removed'})
        except Like.DoesNotExist:
            return Response({'error': 'Like not found'}, status=404)

    @action(detail=False, methods=['post'])
    def invite_family_member(self, request):
        """
        가족 구성원에게 초대 코드를 문자로 전송합니다.
        """
        user = request.user
        family = user.profile.family

        if not family:
            logger.error("가족 정보가 없습니다.")
            return Response({'message': '가족 정보가 없습니다.'}, status=400)

        phone_number = request.data.get('phone_number')
        if not phone_number:
            logger.error("전화번호가 제공되지 않았습니다.")
            return Response({'message': '전화번호가 제공되지 않았습니다.'}, status=400)

        invite_code = str(random.randint(100000, 999999))
        subject = "[모해 - 초대코드]"
        content = f"모해에서 {user.username}님이 가족 구성원 초대 코드를 발송했습니다.\n초대 코드 : {invite_code}"

        presult, wresult = send_sms(subject, content, phone_number, "01083562203")

        if presult or wresult:
            logger.info("초대 코드 문자 전송 성공")
            return Response({'message': '초대 코드 문자 전송 성공', 'invite_code': invite_code})
        else:
            logger.error("초대 코드 문자 전송 실패")
            return Response({'message': '초대 코드 문자 전송 실패'}, status=500)

class FamilyViewSet(viewsets.ModelViewSet):
    queryset = Family.objects.all()
    serializer_class = FamilySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Family.objects.filter(created_by=self.request.user)

    def perform_create(self, serializer):
        family = serializer.save(created_by=self.request.user)
        profile = Profile.objects.get(user=self.request.user)
        profile.family = family
        profile.save()

    def perform_update(self, serializer):
        family = self.get_object()
        if family.created_by != self.request.user:
            raise PermissionDenied('You do not have permission to edit this family.')
        serializer.save()

    def perform_destroy(self, instance):
        family = self.get_object()
        if family.created_by != self.request.user:
            raise PermissionDenied('You do not have permission to delete this family.')
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
        
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def invite_family_member(request):
    user = request.user
    family = user.profile.family

    if not family:
        logger.error("가족 정보가 없습니다.")
        return JsonResponse({'message': '가족 정보가 없습니다.'}, status=400)

    phone_number = request.data.get('phone_number')
    if not phone_number:
        logger.error("전화번호가 제공되지 않았습니다.")
        return JsonResponse({'message': '전화번호가 제공되지 않았습니다.'}, status=400)

    invite_code = str(random.randint(100000, 999999))
    subject = "[모해 - 초대코드]"
    content = f"모해에서 {user.username}님이 가족 구성원 초대 코드를 발송했습니다.\n초대 코드 : {invite_code}"

    presult, wresult = send_sms(subject, content, phone_number, "01083562203")

    if presult or wresult:
        logger.info("초대 코드 문자 전송 성공")
        return JsonResponse({'message': '초대 코드 문자 전송 성공', 'invite_code': invite_code})
    else:
        logger.error("초대 코드 문자 전송 실패")
        return JsonResponse({'message': '초대 코드 문자 전송 실패'}, status=500)