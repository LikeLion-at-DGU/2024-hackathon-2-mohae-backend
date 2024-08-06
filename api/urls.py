from django.urls import path
from .views import AskQuestionView, UserProfileView


app_name = 'api'

urlpatterns = [
    path('ask/', AskQuestionView.as_view(), name='ask-question'),
    path('user_profile/', UserProfileView.as_view(), name='user-profile'),
]
