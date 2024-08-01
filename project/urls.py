from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('cal/', include('cal.urls')),
    path('culture/', include('culture.urls')),
    path('gallery/', include('gallery.urls')),
    path('api/', include('api.urls')),
    path('users/', include('users.urls')),
    path('health/', include('health.urls')),
    path('sms/', include('sms.urls')),  # SMS 관련 URL 포함
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
