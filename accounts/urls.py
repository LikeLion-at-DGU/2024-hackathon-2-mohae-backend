from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import LogoutView, RegisterView, CustomTokenObtainPairView, ProfileView, UpdateProfileView



app_name = 'accounts'

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomTokenObtainPairView.as_view(), name='login'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api-auth/', include('rest_framework.urls')),  # DRF 로그인 뷰 포함
    path('profile/', ProfileView.as_view(), name='profile'),  # 프로필 조회 URL 추가
    path('profile/update/', UpdateProfileView.as_view(), name='profile_update'),  # 프로필 수정 URL 추가
    path('logout/', LogoutView.as_view(), name='logout'),  # 로그아웃 URL 추가
]
