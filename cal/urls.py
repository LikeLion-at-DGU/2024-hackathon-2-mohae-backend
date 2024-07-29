from django.urls import path
from . import views

urlpatterns = [
    path('events/', views.create_event, name='create_event'),
    path('events/<int:pk>/', views.event_detail, name='event_detail'),
    path('events/<int:pk>/update/', views.update_event, name='update_event'),
    path('events/<int:pk>/delete/', views.delete_event, name='delete_event'),
]
