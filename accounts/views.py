import json
import requests
from django.shortcuts import redirect, render
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.http import JsonResponse
from json.decoder import JSONDecodeError
from rest_framework import status
from dj_rest_auth.registration.views import SocialLoginView
from allauth.socialaccount.providers.kakao import views as kakao_view
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from allauth.socialaccount.models import SocialAccount
from .models import User

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

BASE_URL = 'http://localhost:8000/'
KAKAO_CALLBACK_URI = BASE_URL + 'accounts/kakao/login/callback/'

state = getattr(settings, 'STATE')

def login(request):
    return render(request, 'accounts/logintest.html')

def kakao_login(request):
    rest_api_key = settings.KAKAO_REST_API_KEY  # 여기서 KAKAO_REST_API_KEY를 settings에서 가져옴
    return redirect(
        f"https://kauth.kakao.com/oauth/authorize?client_id={rest_api_key}&redirect_uri={KAKAO_CALLBACK_URI}&response_type=code&prompt=login"
    )

def kakao_callback(request):
    rest_api_key = settings.KAKAO_REST_API_KEY  # 여기서 KAKAO_REST_API_KEY를 settings에서 가져옴
    code = request.GET.get("code")
    print("code : " , code)
    redirect_uri = KAKAO_CALLBACK_URI
    """
    Access Token Request
    """
    token_req = requests.get(
        f"https://kauth.kakao.com/oauth/token?grant_type=authorization_code&client_id={rest_api_key}&redirect_uri={redirect_uri}&code={code}")
    token_req_json = token_req.json()

    print("token JSON:", json.dumps(token_req_json, indent=4, ensure_ascii=False))
    error = token_req_json.get("error")
    if error is not None:
        raise JSONDecodeError(error)
    access_token = token_req_json.get("access_token")
    """
    Email Request
    """
    profile_request = requests.get(
        "https://kapi.kakao.com/v2/user/me", headers={"Authorization": f"Bearer {access_token}"})
    profile_json = profile_request.json()

    print("Profile JSON:", json.dumps(profile_json, indent=4, ensure_ascii=False))
    error = profile_json.get("error")
    if error is not None:
        raise JSONDecodeError(error)
    
    kakao_account = profile_json.get('kakao_account')
    # 사용자의 닉네임, 프로필 사진, 섬네일 사진
    properties = profile_json.get('properties')
    """
    kakao_account에서 이메일 외에
    카카오톡 프로필 이미지, 배경 이미지 url 가져올 수 있음
    print(kakao_account) 참고
    """
    # 필요한 정보를 가져옴
    email = kakao_account.get('email')
    # accounts 의 user db 에 입력할 nickname 선언
    nickname = properties.get('nickname')

    """
    Signup or Signin Request
    """
    try:
        user = User.objects.get(email=email)
        # 기존에 가입된 유저의 Provider가 kakao가 아니면 에러 발생, 맞으면 로그인
        # 다른 SNS로 가입된 유저
        social_user = SocialAccount.objects.get(user=user)
        if social_user is None:
            return JsonResponse({'err_msg': 'email exists but not social user'}, status=status.HTTP_400_BAD_REQUEST)
        if social_user.provider != 'kakao':
            return JsonResponse({'err_msg': 'no matching social type'}, status=status.HTTP_400_BAD_REQUEST)
        # 기존에 kakao로 가입된 유저
        data = {'access_token': access_token, 'code': code}
        accept = requests.post(
            f"{BASE_URL}accounts/kakao/login/finish/", data=data)
        accept_status = accept.status_code

        print("try 에서 출력한 status 값 : " , accept_status)

        if accept_status != 200:
            return JsonResponse({'err_msg': 'failed to signin'}, status=accept_status)
        accept_json = accept.json()
        
        userinfo = {
            "email" : user.email,
            "nickname" : user.nickname
        }
        accept_json.pop('user', None)
        accept_json['userinfo'] = userinfo
        
        return JsonResponse(accept_json)
        
    except User.DoesNotExist:
        # 기존에 가입된 유저가 없으면 새로 가입
        data = {'access_token': access_token, 'code': code}

        accept = requests.post(
            f"{BASE_URL}accounts/kakao/login/finish/", data=data)
        accept_status = accept.status_code
        print("except 에서 출력한 status 값 : " , accept_status)
        if accept_status != 200:
            return JsonResponse({'err_msg': 'failed to signup'}, status=accept_status)
        
        # 유저 닉네임을 카카오의 nickname 필드와 동일하게 변경
        user = User.objects.get(email=email)
        user.nickname = nickname
        user.save()
        # Access Token, Refresh token 
        accept_json = accept.json()
        userinfo = {
            "email" : user.email,
            "nickname" : user.nickname
        }
        accept_json.pop('user', None)
        accept_json['userinfo'] = userinfo
        return JsonResponse(accept_json)

class KakaoLogin(SocialLoginView):
    adapter_class = kakao_view.KakaoOAuth2Adapter
    client_class = OAuth2Client
    callback_url = KAKAO_CALLBACK_URI
