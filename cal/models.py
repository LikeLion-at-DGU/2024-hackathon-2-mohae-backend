from django.db import models
from django.contrib.auth.models import User
from .models import Family
# Create your models here.

class Calendar(models.Model):
    STATUS_CHOICES = [
        ('Y', 'Active'),
        ('N', 'Inactive'),
    ]

    event_id = models.AutoField(primary_key=True)  # 일정 인덱스 (Primary Key)
    title = models.CharField(max_length=255, null=False)  # 일정 제목
    description = models.TextField(null=True, blank=True)  # 일정 설명 (옵션)
    type = models.CharField(max_length=255, null=False)  # 일정 유형
    reminder_time = models.DateTimeField(null=True, blank=True)  # 알림 시간 (옵션)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)  # 생성자 (User 테이블 참조)
    family_id = models.ForeignKey(Family, on_delete=models.CASCADE)  # 가족 인덱스 (Family 테이블 참조)
    created_at = models.DateTimeField(auto_now_add=True)  # 생성 시간 (자동 설정)
    updated_at = models.DateTimeField(auto_now=True)  # 수정 시간 (자동 설정)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='Y')  # 상태 ('Y': 활성, 'N': 비활성)

    def __str__(self):
        return self.title  # 객체를 문자열로 표현할 때 일정 제목 반환