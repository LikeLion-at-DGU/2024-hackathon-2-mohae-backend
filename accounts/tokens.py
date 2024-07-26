from datetime import timedelta
from rest_framework_simplejwt.tokens import RefreshToken

def generate_jwt_token(user):
    refresh = RefreshToken.for_user(user)
    access_token = str(refresh.access_token)

    # 토큰 만료 시간 설정 (2시간)
    refresh.set_exp(lifetime=timedelta(hours=2))

    return {
        'refresh': str(refresh),
        'access': access_token,
    }
