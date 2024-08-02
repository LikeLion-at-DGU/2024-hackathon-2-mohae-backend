from datetime import timezone
from django.db import models
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

User = get_user_model()

# 카테고리 모델
class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)  # 카테고리 이름

    def __str__(self):
        return self.name

# 하위 카테고리 모델
class SubCategory(models.Model):
    category = models.ForeignKey(Category, related_name='subcategories', on_delete=models.CASCADE)  # 연결된 카테고리
    name = models.CharField(max_length=255)  # 하위 카테고리 이름

    def __str__(self):
        return self.name

# 문화 활동 모델
class CulturalActivity(models.Model):
    title = models.CharField(max_length=255, null=False)  # 활동 제목
    description = models.TextField(null=True, blank=True)  # 활동 설명
    start_date = models.DateTimeField(null=True)  # 시작 일자
    end_date = models.DateTimeField(null=True)  # 종료 일자
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True)  # 생성한 사용자
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True)  # 가격
    available_slots = models.PositiveIntegerField(default=1, null=True)  # 예약 가능 슬롯 수
    created_at = models.DateTimeField(auto_now_add=True)  # 생성된 시간
    updated_at = models.DateTimeField(auto_now=True)  # 마지막 업데이트 시간
    status = models.CharField(max_length=1, choices=[('Y', 'Active'), ('N', 'Inactive')], default='Y', null=True)  # 활동 상태
    category = models.ForeignKey(Category, related_name='activities', on_delete=models.CASCADE, null=True)  # 연결된 카테고리
    subcategory = models.ForeignKey(SubCategory, related_name='activities', on_delete=models.CASCADE, null=True)  # 연결된 하위 카테고리
    thumbnail = models.ImageField(upload_to='thumbnails/', null=True, blank=True)  # 썸네일 이미지 추가
    hyperlink = models.URLField(max_length=200, null=True, blank=True)  # 하이퍼링크 추가
    location = models.CharField(max_length=255, null=True, blank=True)  # 위치 추가
    distance = models.TextField(null=True, blank=True)  # 잡다한 정보 필드 추가

    def __str__(self):
        return self.title

    def clean(self):
        if self.start_date and self.start_date < timezone.now():
            raise ValidationError('Start date cannot be in the past.')
        if self.end_date and self.start_date and self.end_date <= self.start_date:
            raise ValidationError('End date must be after start date.')

# 예약 모델
class Reservation(models.Model):
    activity = models.ForeignKey(CulturalActivity, on_delete=models.CASCADE)  # 예약된 활동
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # 예약한 사용자
    reserved_at = models.DateTimeField(auto_now_add=True)  # 예약된 시간
    STATUS_CHOICES = [
        ('P', 'Pending'),
        ('C', 'Confirmed'),
        ('N', 'Cancelled'),
    ]
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='P')  # 예약 상태
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='P')  # 예약 상태

    def __str__(self):
        return f"Reservation for {self.activity.title} by {self.user.email}"

# 확정된 예약 모델
class ConfirmedReservation(models.Model):
    reservation = models.OneToOneField(Reservation, on_delete=models.CASCADE)  # 연결된 예약
    confirmed_at = models.DateTimeField(auto_now_add=True)  # 확정된 시간
    reservation = models.OneToOneField(Reservation, on_delete=models.CASCADE)  # 연결된 예약
    confirmed_at = models.DateTimeField(auto_now_add=True)  # 확정된 시간

    def __str__(self):
        return f"Confirmed reservation for {self.reservation.activity.title} by {self.reservation.user.email}"

# 좋아요 모델
class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # 좋아요를 누른 사용자
    activity = models.ForeignKey(CulturalActivity, on_delete=models.CASCADE)  # 좋아요를 받은 활동
    liked_at = models.DateTimeField(auto_now_add=True)  # 좋아요를 누른 시간

    def __str__(self):
        return f"{self.user.email} likes {self.activity.title}"