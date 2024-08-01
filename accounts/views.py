from rest_framework import generics
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth.models import User
from .serializers import RegisterSerializer, CustomTokenObtainPairSerializer
from rest_framework.response import Response
from rest_framework import status

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        user = User.objects.get(username=response.data['username'])
        refresh = RefreshToken.for_user(user)
        response.data['refresh'] = str(refresh)
        response.data['access'] = str(refresh.access_token)
        return response

class CustomLoginView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_401_UNAUTHORIZED)
        
        user = User.objects.get(email=request.data['email'])
        refresh = RefreshToken.for_user(user)
        
        response = Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_200_OK)
        
        # 쿠키 설정
        response.set_cookie(
            key='access_token',
            value=str(refresh.access_token),
            httponly=True,
            secure=False,  # 배포 시 True로 변경
            samesite='Lax',
        )
        
        return response