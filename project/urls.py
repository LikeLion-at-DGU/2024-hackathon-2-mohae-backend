from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('dj_rest_auth.urls')),
    path('accounts/', include('accounts.urls')),    
    path('cal/',include('cal.urls')),
    path('culture/', include('culture.urls')),
    path('gallery/',include('gallery.urls')),
    path('api/', include('api.urls')),
    path('users/',include('users.urls')),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
