from django.urls import path
from .views import emergency_button_pressed, send_general_sms


app_name = 'sms'

urlpatterns = [
    path('emergency/', emergency_button_pressed, name='emergency_button_pressed'),
    path('send/', send_general_sms, name='send_general_sms'),
]
