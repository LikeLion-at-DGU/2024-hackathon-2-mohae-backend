# fix_foreign_keys.py

import os
import django

# Django 설정 파일 경로 설정
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

from users.models import Family
from django.contrib.auth import get_user_model

User = get_user_model()

# 잘못된 외래 키 참조 삭제
def fix_foreign_keys():
    invalid_families = Family.objects.exclude(created_by__in=User.objects.all())
    count = invalid_families.count()
    invalid_families.delete()
    print(f"{count} invalid foreign key references deleted.")

if __name__ == '__main__':
    fix_foreign_keys()
