from django.contrib import admin
from .models import Album, Photo, Video, PhotoVideoLike, Comment, Favorite
# Register your models here.


admin.site.register(Album)
admin.site.register(Photo)
admin.site.register(Video)
admin.site.register(PhotoVideoLike)
admin.site.register(Comment)
admin.site.register(Favorite)