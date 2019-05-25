from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.validators import FileExtensionValidator
from django.core.validators import validate_image_file_extension

class Profile(models.Model):
    dp = models.ImageField(upload_to='profile_pictures/', default="profile_pictures/no_dp.png", validators=[FileExtensionValidator(allowed_extensions=['jpg', 'png', 'jpeg'])])
    dob = models.DateField(default=timezone.now)
    bio = models.CharField(max_length=100, default="No bio")
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

class Album(models.Model):
    title = models.CharField(max_length=40)
    description = models.TextField(default="No Description...")
    cover_dp = models.ImageField(upload_to='album_cover_pictures/', default="album_cover_pictures/no_cover_dp.png", validators=[FileExtensionValidator(allowed_extensions=['jpg', 'png', 'jpeg'])])
    date = models.DateField(auto_now_add=True)
    time = models.TimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class Music(models.Model):
    title = models.CharField(max_length=75)
    description = models.TextField(default="No Description...")
    file = models.FileField(upload_to='music/', validators=[FileExtensionValidator(allowed_extensions=['mp3', 'ogg', 'wav'])])
    date = models.DateField(auto_now_add=True)
    time = models.TimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    album = models.ForeignKey(Album, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class Video(models.Model):
    thumbnail = models.ImageField(upload_to='thumbnails/', default="thumbnails/no_thumb.png", validators=[FileExtensionValidator(allowed_extensions=['jpg', 'png', 'jpeg'])])
    title = models.CharField(max_length=75)
    description = models.TextField(default="No Description...")
    file = models.FileField(upload_to='videos/', validators=[FileExtensionValidator(allowed_extensions=['mp4', 'flv'])])
    date = models.DateField(auto_now_add=True)
    time = models.TimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    views = models.IntegerField(default=0)
    album = models.ForeignKey(Album, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class LikeAlbum(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_time = models.DateTimeField(auto_now_add=True)
    album = models.ForeignKey(Album, on_delete=models.CASCADE)

    def __str__(self):
        return self.album.title + " - " + self.user.username

class LikeMusic(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_time = models.DateTimeField(auto_now_add=True)
    music = models.ForeignKey(Music, on_delete=models.CASCADE)

    def __str__(self):
        return self.music.album.title + " - " + self.music.title + " - " + self.user.username

class LikeVideo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_time = models.DateTimeField(auto_now_add=True)
    video = models.ForeignKey(Video, on_delete=models.CASCADE)

    def __str__(self):
        return self.video.album.title + " - " + self.video.title + " - " + self.user.username

class CommentAlbum(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_time = models.DateTimeField(auto_now_add=True)
    album = models.ForeignKey(Album, on_delete=models.CASCADE)
    text = models.TextField()

    def __str__(self):
        return self.album.title + " - " + self.user.username

class CommentMusic(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_time = models.DateTimeField(auto_now_add=True)
    music = models.ForeignKey(Music, on_delete=models.CASCADE)
    text = models.TextField()

    def __str__(self):
        return self.music.album.title + " - " + self.music.title + " - " + self.user.username

class CommentVideo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_time = models.DateTimeField(auto_now_add=True)
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    text = models.TextField()

    def __str__(self):
        return self.video.album.title + " - " + self.video.title + " - " + self.user.username
