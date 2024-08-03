from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.models import User
from users.models import Family
from accounts.models import Profile
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from .sms_service import send_sms
import logging

# 로그 설정
logger = logging.getLogger(__name__)

# 긴급 상황 알림 메시지 설정
subject = "긴급상황 발생"
content = "긴급상황이 발생했습니다. 즉시 확인 바랍니다."
callback = "01083562203"  # 발신자 전화번호

def get_family_members_phone_numbers(user):
    """
    주어진 사용자(user)에 해당하는 가족 구성원의 전화번호 목록을 반환합니다.
    """
    family = user.profile.family
    if not family:
        logger.error("가족 정보가 없습니다.")
        return []
    
    family_members = Profile.objects.filter(family=family).exclude(user=user)
    phone_numbers = [member.phone_number for member in family_members if member.phone_number]
    logger.debug(f"가족 구성원의 전화번호: {phone_numbers}")
    return phone_numbers

def send_emergency_sms(user):
    """
    긴급 상황 발생 시 가족 구성원에게 문자 메시지를 전송합니다.
    """
    phone_numbers = get_family_members_phone_numbers(user)
    
    if not phone_numbers:
        logger.error("가족 구성원 목록이 비어 있거나 가족 구성원의 전화번호가 없습니다.")
        return "가족 구성원 목록이 비어 있거나 가족 구성원의 전화번호가 없습니다."

    for hpno in phone_numbers:
        presult, wresult = send_sms(subject, content, hpno, callback)
        if not (presult or wresult):
            logger.error(f"{hpno}로 문자 전송 실패")
            return f"{hpno}로 문자 전송 실패"
    
    logger.info("문자 전송 성공")
    return "문자 전송 성공"

@csrf_exempt
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def emergency_button_pressed(request):
    """
    긴급 버튼이 눌렸을 때 호출되는 뷰.
    현재 로그인된 사용자의 가족 구성원에게 긴급 메시지를 보냅니다.
    """
    user = request.user
    message = send_emergency_sms(user)
    logger.debug(f"긴급 버튼 눌림: {message}")
    return JsonResponse({'message': message})

@csrf_exempt
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def send_general_sms(request):
    """
    일반 SMS를 전송하는 뷰.
    """
    if request.method == 'POST':
        subject = request.data.get('subject', '일반 알림')
        content = request.data.get('content', '일반 메시지 내용')
        hpno = request.data.get('hpno')
        
        if not hpno:
            logger.error("전화번호가 제공되지 않았습니다.")
            return JsonResponse({'message': '전화번호가 제공되지 않았습니다.'}, status=400)
        
        presult, wresult = send_sms(subject, content, hpno, callback)
        
        if presult or wresult:
            logger.info("문자 전송 성공")
            return JsonResponse({'message': '문자 전송 성공'})
        else:
            logger.error("문자 전송 실패")
            return JsonResponse({'message': '문자 전송 실패'}, status=500)
    logger.error("잘못된 요청 방식입니다.")
    return JsonResponse({'message': '잘못된 요청 방식입니다.'}, status=405)
