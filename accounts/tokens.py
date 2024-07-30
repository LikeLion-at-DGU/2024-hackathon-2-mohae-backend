from datetime import timedelta
from rest_framework_simplejwt.tokens import RefreshToken


#주어진 사용자에 대해 JWT 토큰을 생성. 여기서 리프레시 토큰과 액세스 토큰이 반환됨

def generate_jwt_token(user):
    refresh = RefreshToken.for_user(user)
    access_token = str(refresh.access_token)

    # 토큰 만료 시간 설정 (2시간)
    refresh.set_exp(lifetime=timedelta(hours=2))

    return {
        'refresh': str(refresh),
        'access': access_token,
    }
