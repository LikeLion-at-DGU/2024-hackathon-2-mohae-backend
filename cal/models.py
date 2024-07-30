from django.db import models
from django.contrib.auth.models import User
from users.models import Family
from django.utils import timezone

class Calendar(models.Model):
    event_id = models.AutoField(primary_key=True)  # 일정 인덱스 (Primary Key)
    title = models.CharField(max_length=255, null=False)  # 일정 제목
    start = models.DateTimeField(null=False)  # 일정 시작 시간
    end = models.DateTimeField(default=timezone.now, null=False)  # 일정 종료 시간
    participants = models.ManyToManyField(User, related_name='calendar_events', blank=True)  # 참여자 (ManyToManyField로 변경)
    emoji = models.TextField(null=True, blank=True)  # 이모지 필드 추가
    emoji_text = models.TextField(null=True, blank=True)  # 이모지 텍스트 필드 추가
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_events')  # 생성자 (User 테이블 참조)
    family_id = models.ForeignKey(Family, on_delete=models.CASCADE)  # 가족 인덱스 (Family 테이블 참조)
    created_at = models.DateTimeField(auto_now_add=True)  # 생성 시간 (자동 설정)
    updated_at = models.DateTimeField(auto_now=True)  # 수정 시간 (자동 설정)
    status = models.CharField(max_length=1, default='Y', null=False)  # 상태 ('Y': 활성, 'N': 비활성)

    def __str__(self):
        return self.title  # 객체를 문자열로 표현할 때 일정 제목 반환
