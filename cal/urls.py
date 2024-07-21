from django.urls import path
from . import views

urlpatterns = [
    path('calendar/', views.list_events, name='list_events'),  # 일정 목록 조회
    path('calendar/<int:pk>/', views.event_detail, name='event_detail'),  # 일정 상세 조회
    path('calendar/create/', views.create_event, name='create_event'),  # 일정 생성
    path('calendar/update/<int:pk>/', views.update_event, name='update_event'),  # 일정 수정
    path('calendar/delete/<int:pk>/', views.delete_event, name='delete_event'),  # 일정 삭제
]
