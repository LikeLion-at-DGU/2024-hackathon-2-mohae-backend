from django.urls import path
from . import views

urlpatterns = [
    path('activities/', views.cultural_activities, name='cultural_activities'),
    path('activities/<int:activity_id>/reserve/', views.reserve_activity, name='reserve_activity'),
]
