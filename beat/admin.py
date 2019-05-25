from django.contrib import admin
from .models import Album, Profile, Music, Video, LikeAlbum, LikeMusic, LikeVideo, CommentAlbum, CommentMusic, CommentVideo

admin.site.register(Album)
admin.site.register(Profile)
admin.site.register(Music)
admin.site.register(Video)
admin.site.register(LikeAlbum)
admin.site.register(LikeMusic)
admin.site.register(LikeVideo)
admin.site.register(CommentAlbum)
admin.site.register(CommentMusic)
admin.site.register(CommentVideo)
