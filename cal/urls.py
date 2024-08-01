from django.urls import path
from . import views

urlpatterns = [
    path('events/', views.create_event, name='create_event'),
    path('events/list/', views.list_events, name='list_events'),  # 이벤트 목록 조회 추가
    path('events/<int:pk>/', views.event_detail, name='event_detail'),
    path('events/<int:pk>/update/', views.update_event, name='update_event'),
    path('events/<int:pk>/delete/', views.delete_event, name='delete_event'),
    path('family/<int:family_id>/members/', views.family_members, name='family_members'),  # 가족 구성원 목록 조회 추가
]
