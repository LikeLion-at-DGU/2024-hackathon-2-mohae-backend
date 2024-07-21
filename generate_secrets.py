import os
import json
import binascii
from django.core.management.utils import get_random_secret_key

# 파일 경로 설정
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
secrets_file = os.path.join(BASE_DIR, 'secrets.json')

# secrets.json 파일 내용 생성
secrets = {
    "SECRET_KEY": get_random_secret_key(),
    "STATE": binascii.hexlify(os.urandom(16)).decode()
}

# JSON 파일로 저장
with open(secrets_file, 'w') as f:
    json.dump(secrets, f, indent=4)

print(f"secrets.json 파일이 생성되었습니다: {secrets_file}")