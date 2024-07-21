from django.db import models

# Create your models here.
class Family(models.Model):
    STATUS_CHOICES = [
        ('Y', 'Active'),
        ('N', 'Inactive'),
    ]

    family_id = models.AutoField(primary_key=True)  # 가족 인덱스 (Primary Key)
    family_name = models.CharField(max_length=255, null=False)  # 가족 이름
    created_at = models.DateTimeField(auto_now_add=True)  # 생성 시간 (자동 설정)
    updated_at = models.DateTimeField(auto_now=True)  # 수정 시간 (자동 설정)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='Y')  # 상태 ('Y': 활성, 'N': 비활성)

    def __str__(self):
        return self.family_name  # 객체를 문자열로 표현할 때 가족 이름 반환