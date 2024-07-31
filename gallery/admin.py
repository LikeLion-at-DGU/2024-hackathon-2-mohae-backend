from django.contrib import admin
from .models import Album, Photo, Comment, Favorite
# Register your models here.


admin.site.register(Album)
admin.site.register(Photo)
admin.site.register(Comment)
admin.site.register(Favorite)