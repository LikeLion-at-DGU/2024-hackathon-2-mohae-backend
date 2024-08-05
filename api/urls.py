from django.urls import path
from .views import AskQuestionView, UserProfileView, RandomQuestionsView

urlpatterns = [
    path('ask/', AskQuestionView.as_view(), name='ask-question'),
    path('user_profile/', UserProfileView.as_view(), name='user-profile'),
    path('random_questions/', RandomQuestionsView.as_view(), name='random-questions'),
]
