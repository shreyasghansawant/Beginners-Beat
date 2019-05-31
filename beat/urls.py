from django.urls import path
from . import views

app_name = "beat"

urlpatterns = [
    path('signup/', views.signup_form, name="signup"),
    path('login/', views.login_form, name="login"),
    path('logout/', views.logout_form, name="logout"),
    path('api/user/', views.api_user, name="api-user"),
    path('change/password/', views.change_password, name="change-password"),
    path('edit/profile/', views.edit_profile, name="edit-profile"),
    path('my-profile/', views.my_profile, name="my-profile"),
    path('profile/profile_id=<int:user_id>/', views.profile, name="profile"), #
    path('liked-albums-videos/', views.liked_albums_videos, name="liked-albums"),
    path('delete/account/', views.delete_user, name="delete-user"),
    path('add/album/', views.add_album, name="add-album"),
    path('edit/album/album_id=<int:album_id>/', views.update_album, name="update-album"), #
    path('delete/album/album_id=<int:album_id>/', views.delete_album, name="delete-album"), #
    path('edit/album-music-videos/album_id=<int:album_id>/', views.edit_album, name="edit-album"), #
    path('add/music/album_id=<int:album_id>/', views.add_music, name="add-music"), #
    path('edit/music/music_id=<int:music_id>/', views.update_music, name="update-music"), #
    path('delete/music/music_id=<int:music_id>/', views.delete_music, name="delete-music"), #
    path('add/video/album_id<int:album_id>/', views.add_video, name="add-video"), #
    path('edit/video/video_id=<int:video_id>/', views.update_video, name="update-video"), #
    path('delete/video/video_id=<int:video_id>/', views.delete_video, name="delete-video"), #
    path('', views.index, name="index"),
    path('album_id=<int:album_id>/', views.detail, name="detail"), #
    #path('music_id=<int:music_id>/', views.detail_music, name="detail-music"), #
    path('video_id=<int:video_id>/', views.detail_video, name="detail-video"), #
    path('like/album/album_id<int:album_id>/', views.like_album, name="like-album"), #
    path('like/music/music_id=<int:music_id>/', views.like_music, name="like-music"), #
    path('like/video/video_id=<int:video_id>/', views.like_video, name="like-video"), #
    path('comment/album/album_id=<int:album_id>/', views.comment_album, name="comment-album"), #
    path('comment/music/music_id=<int:music_id>/', views.comment_music, name="comment-music"), #
    path('comment/video/video_id=<int:video_id>/', views.comment_video, name="comment-video"), #
    path('album/album_id=<int:album_id>/delete/comment/comment_id=<int:comment_id>/', views.delete_comment_album, name="delete-comment-album"), ##
    path('music/music_id=<int:music_id>/delete/comment/comment_id=<int:comment_id>/', views.delete_comment_music, name="delete-comment-music"), ##
    path('video/video_id=<int:video_id>/delete/comment/comment_id=<int:comment_id>/', views.delete_comment_video, name="delete-comment-video"), ##
    path('search/', views.search, name="search"),
    path('about/', views.about, name="about"),
    path('album/album_id=<int:album_id>/liked_by/', views.liked_by_album, name="liked-by-album"), #
    path('video/video_id=<int:video_id>/liked_by/', views.liked_by_video, name="liked-by-video"), #
]
