from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),  # 단일 경로로 관리
    path('cal/', include('cal.urls')),
    path('culture/', include('culture.urls')),
    path('gallery/', include('gallery.urls')),
    path('api/', include('api.urls')),
    path('users/', include('users.urls')),
    path('health/', include('health.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
