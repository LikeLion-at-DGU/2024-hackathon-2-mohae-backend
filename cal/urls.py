from django.urls import path
from . import views


app_name = 'cal'

urlpatterns = [
    path('events/', views.create_event, name='create_event'),
    path('events/list/', views.list_events, name='list_events'),  # 이벤트 목록 조회 추가
    path('events/<int:pk>/', views.event_detail, name='event_detail'),
    path('events/<int:pk>/update/', views.update_event, name='update_event'),
    path('events/<int:pk>/delete/', views.delete_event, name='delete_event'),
    path('family/<int:family_id>/members/', views.family_members, name='family_members'),  # 가족 구성원 목록 조회 추가
    path('events/family/<int:family_id>/member/<int:member_id>/', views.family_member_events, name='family_member_events'),  # 가족 구성원별 일정 조회 추가
    path('health/family/<int:family_id>/daily/<int:member_id>/', views.daily_health_data, name='daily_health_data'),  # 가족 구성원의 당일 건강 데이터 조회 추가
]
