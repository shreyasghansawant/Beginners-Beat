from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from .models import Album, Profile, Music, Video, CommentAlbum, CommentMusic, CommentVideo, LikeAlbum, LikeMusic, LikeVideo
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from .forms import SignUpForm, ProfileForm, AlbumForm, MusicForm, VideoForm, UserEditForm
from django.conf import settings
from django.core.mail import send_mail
from django.contrib import messages

def signup_form(request):
    storage = messages.get_messages(request)
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            all_users = User.objects.all()
            for one_user in all_users:
                if one_user.email == instance.email:
                    messages.error(request, 'This email is taken by another account.')
                    return redirect('beat:signup')
            user = form.save()
            #profile = Profile.objects.create(user=user)
            #profile.save()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            messages.success(request, "Welcome to Beginner's Beat, Your account is created successfully!")
            return redirect('beat:edit-profile')
    else:
        form = SignUpForm()
    return render(request, 'beat/signup.html', {
            'form': form,
            'messages': storage,
        })

def login_form(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            subject = "You Just Logged in to Beginner's Beat"
            text = "If it wasn't you, Just email us your username on this email address; We will take action as quick as we can.\nThank you"
            me = settings.EMAIL_HOST_USER
            send_mail(subject, text, me, [user.email,], fail_silently=True)
            return redirect('beat:index')
    else:
        form = AuthenticationForm()
    return render(request, 'beat/login.html', {'form': form})

@login_required(login_url="beat:login")
def logout_form(request):
    if request.method == "POST":
        logout(request)
        return redirect('beat:index')

@login_required(login_url="beat:login")
def api_user(request):
    try:
        profile = Profile.objects.get(user=request.user)
        if profile:
            user = request.user
            subject = "You Just Logged in to Beginner's Beat using API service of Google, Github or Facebook"
            text = "If it wasn't you, Just email us your username on this email address; We will take action as quick as we can.\nThank you"
            me = settings.EMAIL_HOST_USER
            send_mail(subject, text, me, [user.email,], fail_silently=True)
            return redirect('beat:index')
    except Exception:
        return redirect('beat:edit-profile')

@login_required(login_url="beat:login")
def change_password(request):
    if request.method == "POST":
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Password Changed Successfully!')
            update_session_auth_hash(request, form.user)
            return redirect('beat:my-profile')
        #else:
            #messages.error(request, 'Error Occured, Retry!')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'beat/change_password.html', {'form': form})

@login_required(login_url="beat:login")
def edit_profile(request):
    storage = messages.get_messages(request)
    try:
        profile = Profile.objects.get(user=request.user)
        if profile:
            if request.method == "POST":
                form = ProfileForm(request.POST or None, request.FILES or None, instance=profile)
                form_user = UserEditForm(request.POST or None, instance=request.user)
                if form.is_valid() and form_user.is_valid():
                    form.save()
                    form_user.save()
                    messages.success(request, "Profile Updated Successfully!")
                    return redirect('beat:my-profile')
            else:
                form = ProfileForm(instance=profile)
                form_user = UserEditForm(instance=request.user)
            return render(request, 'beat/edit_profile.html', {
                'form': form,
                'form_user': form_user,
                'messages': storage,
            })
    except Exception:
        new_profile = Profile.objects.create(user=request.user)
        new_profile.save()
        user = request.user
        subject = "Welcome to Beignner's Beat"
        text = "Hello " + user.first_name + ", \n\nThank you for joining us.\nYour Beginner's Beat account has been successfully created. \n\nListen to the music of beginner's (maybe the future composers/artists) and enjoy it."
        me = settings.EMAIL_HOST_USER
        send_mail(subject, text, me, [user.email,], fail_silently=True)
        messages.success(request, "Welcome to Beginner's Beat, Your account is created successfully!")
        return redirect('beat:edit-profile')

@login_required(login_url="beat:login")
def my_profile(request):
    user = request.user
    storage = messages.get_messages(request)
    albums = Album.objects.filter(author=user).order_by('-date', '-time')
    musics = Music.objects.filter(author=user)
    return render(request, 'beat/my_profile.html', {
        'user': user,
        'albums': albums,
        'musics': musics,
        'messages': storage,
    })

def profile(request, user_id):
    #user = User.objects.get(pk=user_id)
    p_user = get_object_or_404(User, pk=user_id)
    if p_user == request.user:
        return redirect('beat:my-profile')
    albums = Album.objects.filter(author=p_user).order_by('-date', '-time')
    musics = Music.objects.filter(author=p_user)
    return render(request, 'beat/profile.html', {
        'p_user': p_user,
        'albums': albums,
        'musics': musics,
    })

def liked_albums_videos(request):
    liked = LikeAlbum.objects.filter(user=request.user).order_by('-date_time')
    liked_videos = LikeVideo.objects.filter(user=request.user).order_by('-date_time')
    return render(request, 'beat/liked_albums_videos.html', {
        'liked': liked,
        'liked_videos': liked_videos,
    })

@login_required(login_url="beat:login")
def delete_user(request):
    if request.method == "POST":
        if request.user:
            request.user.delete()
            return redirect('beat:index')

@login_required(login_url="beat:login")
def add_album(request):
    if request.method == "POST":
        form = AlbumForm(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.author = request.user
            instance.save()
            return redirect('beat:edit-album', instance.id)
    else:
        form = AlbumForm()
    return render(request, 'beat/add_album.html', {'form': form})

@login_required(login_url="beat:login")
def update_album(request, album_id):
    #album = Album.objects.get(pk=album_id)
    album = get_object_or_404(Album, pk=album_id)
    if request.method == "POST":
        form = AlbumForm(request.POST or None, request.FILES or None, instance=album)
        if form.is_valid():
            form.save()
            messages.success(request, "Album Updated Successfully!")
            return redirect('beat:edit-album', album.id)
    else:
        form = AlbumForm(instance=album)
    return render(request, 'beat/add_album.html', {
        'form': form,
        'updateit': "yes",
    })

@login_required(login_url="beat:login")
def delete_album(request, album_id):
    if request.method == "POST":
        #album = Album.objects.get(pk=album_id)
        album = get_object_or_404(Album, pk=album_id)
        if album.author == request.user:
            album.delete()
            messages.success(request, "Album Deleted Successfully!")
            return redirect('beat:my-profile')

@login_required(login_url="beat:login")
def edit_album(request, album_id):
    #user = request.user
    #album = Album.object.get(pk=album_id)
    #album = get_object_or_404(Album, pk=album_id)
    #if album.author == user:
        #musics = Music.objects.filter(album=album, author=user)
        #videos = Video.objects.filter(album=album, author=user)
        #likes = LikeAlbum.objects.filter(album=album).count()
        #num_comments = CommentAlbum.objects.filter(album=album).count()
        #comments = CommentAlbum.objects.filter(album=album)
        #return render(request, 'beat/detail.html', {
            #'album': album,
            #'musics': musics,
            #'videos': videos,
            #'likes': likes,
            #'num_comments': num_comments,
            #'comments': comments,
            #'user': user,
        #})
    ###############################################################
    user = request.user
    storage = messages.get_messages(request)
    #album = Album.objects.get(pk=album_id)
    album = get_object_or_404(Album, pk=album_id)
    if album.author == user:
        likes = LikeAlbum.objects.filter(album=album).count()
        num_comments = CommentAlbum.objects.filter(album=album).count()
        comments = CommentAlbum.objects.filter(album=album).order_by('-date_time')
        musics = Music.objects.filter(album=album).order_by('-date', '-time')
        videos = Video.objects.filter(album=album).order_by('-date', '-time')
        un_like = None
        try:
            liked = LikeAlbum.objects.filter(album=album, user=request.user)
            if liked:
                un_like = "liked"
        except Exception:
            un_like = "not liked"
        return render(request, 'beat/edit_album.html', {
            'album': album,
            'musics': musics,
            'videos': videos,
            'likes': likes,
            'num_comments': num_comments,
            'comments': comments,
            'un_like': un_like,
            'user': user,
            'messages': storage,
        })

@login_required(login_url="beat:login")
def add_music(request, album_id):
    album = Album.objects.get(pk=album_id)
    if request.user == album.author:
        if request.method == "POST":
            form = MusicForm(request.POST, request.FILES)
            if form.is_valid():
                instance = form.save(commit=False)
                instance.author = request.user
                instance.album = album
                instance.save()
                messages.success(request, "Music Added Successfully!")
                return redirect('beat:edit-album', album.id)
        else:
            form = MusicForm()
        return render(request, 'beat/add_music.html', {
            'form': form,
            'album': album,
        })

@login_required(login_url="beat:login")
def update_music(request, music_id):
    #music = Music.objects.get(pk=music_id)
    music = get_object_or_404(Music, pk=music_id)
    if request.user == music.author:
        if request.method == "POST":
            form = MusicForm(request.POST or None, request.FILES or None, instance=music)
            if form.is_valid():
                form.save()
                messages.success(request, "Musics Updated Successfully!")
                return redirect('beat:edit-album', music.album.id)
        else:
            form = MusicForm(instance=music)
        return render(request, 'beat/add_music.html', {
            'form': form,
            'updateit': "yes",
        })

@login_required(login_url="beat:login")
def delete_music(request, music_id):
    if request.method == "POST":
        #music = Music.objects.get(pk=music_id)
        music = get_object_or_404(Music, pk=music_id)
        if music.author == request.user:
            music.delete()
            messages.success(request, "Music Deleted Successfully!")
            return redirect('beat:edit-album', music.album.id)

@login_required(login_url="beat:login")
def add_video(request, album_id):
    album = Album.objects.get(pk=album_id)
    if request.user == album.author:
        if request.method == "POST":
            form = VideoForm(request.POST, request.FILES)
            if form.is_valid():
                instance = form.save(commit=False)
                instance.author = request.user
                instance.album = album
                instance.save()
                return redirect('beat:detail-video', instance.id)
        else:
            form = VideoForm()
        return render(request, 'beat/add_video.html', {
            'form': form,
            'album': album,
        })

@login_required(login_url="beat:login")
def update_video(request, video_id):
    #video = Video.objects.get(pk=video_id)
    video = get_object_or_404(Video, pk=video_id)
    if request.user == video.author:
        if request.method == "POST":
            form = VideoForm(request.POST or None, request.FILES or None, instance=video)
            if form.is_valid():
                form.save()
                messages.success(request, "Video Updated Successfully!")
                return redirect('beat:detail-video', video.id)
        else:
            form = VideoForm(instance=video)
        return render(request, 'beat/add_video.html', {
            'form': form,
            'updateit': "yes",
        })

@login_required(login_url="beat:login")
def delete_video(request, video_id):
    if request.method == "POST":
        #video = Video.objects.get(pk=video_id)
        video = get_object_or_404(Video, pk=video_id)
        if video.author == request.user:
            video.delete()
            messages.success(request, "Video Deleted Successfully!")
            return redirect('beat:edit-album', video.album.id)

def index(request):
    albums = Album.objects.all().order_by('-date', '-time')
    users = User.objects.all().order_by('?')
    musics = Music.objects.all().order_by('?')
    #albums = get_list_or_404(Album.objects.order_by('-date', '-time'))
    #users = get_list_or_404(User.objects.order_by('?'))
    #musics = get_list_or_404(Music.objects.order_by('?'))
    return render(request, 'beat/index.html', {
        'albums': albums,
        'users': users,
        'musics': musics,
    })

def detail(request, album_id):
    storage = messages.get_messages(request)
    user = request.user
    #album = Album.objects.get(pk=album_id)
    album = get_object_or_404(Album, pk=album_id)
    if user == album.author:
        return redirect('beat:edit-album', album.id)
    likes = LikeAlbum.objects.filter(album=album).count()
    num_comments = CommentAlbum.objects.filter(album=album).count()
    comments = CommentAlbum.objects.filter(album=album).order_by('-date_time')
    musics = Music.objects.filter(album=album).order_by('-date', '-time')
    videos = Video.objects.filter(album=album).order_by('-date', '-time')
    un_like = None
    try:
        liked = LikeAlbum.objects.filter(album=album, user=request.user)
        if liked:
            un_like = "liked"
    except Exception:
        un_like = "not liked"
    return render(request, 'beat/detail.html', {
        'album': album,
        'musics': musics,
        'videos': videos,
        'likes': likes,
        'num_comments': num_comments,
        'comments': comments,
        'un_like': un_like,
        'user': user,
        'messages': storage,
    })

'''
Will use it later
def detail_music(request, music_id):
    #music = Music.objects.get(pk=music_id)
    music = get_object_or_404(Music, pk=music_id)
    likes = LikeMusic.objects.filter(music=music).count()
    num_comments = CommentMusic.objects.filter(music=music).count()
    comments = CommentMusic.objects.filter(music=music)
    un_like = None
    try:
        liked = LikeMusic.objects.filter(music=music, user=request.user)
        if liked:
            un_like = "liked"
    except Exception:
        un_like = "not liked"
    return render(request, 'beat/detail_music.html', {
        'music': music,
        'likes': likes,
        'num_comments': num_comments,
        'comments': comments,
        'un_like': un_like,
    })
'''

def detail_video(request, video_id):
    storage = messages.get_messages(request)
    #video = Video.objects.get(pk=video_id)
    video = get_object_or_404(Video, pk=video_id)
    video.views += 1
    video.save()
    album = get_object_or_404(Album, pk=video.album.id)
    more_videos = Video.objects.filter(album=album).order_by('?')
    more_user_videos = Video.objects.filter(author=album.author).order_by('?')
    all_more_videos = get_list_or_404(Video)
    likes = LikeVideo.objects.filter(video=video).count()
    num_comments = CommentVideo.objects.filter(video=video).count()
    comments = CommentVideo.objects.filter(video=video).order_by('-date_time')
    un_like = None
    try:
        liked = LikeVideo.objects.filter(video=video, user=request.user)
        if liked:
            un_like = "liked"
    except Exception:
        un_like = "not liked"
    return render(request, 'beat/detail_video.html', {
        'video': video,
        'likes': likes,
        'num_comments': num_comments,
        'comments': comments,
        'un_like': un_like,
        'more_videos': more_videos,
        'album': album,
        'more_user_videos': more_user_videos,
        'all_more_videos': all_more_videos,
        'messages': storage,
    })

@login_required(login_url="beat:login")
def like_album(request, album_id):
    if request.method == "POST":
        #album = Album.objects.get(pk=album_id)
        album = get_object_or_404(Album, pk=album_id)
        try:
            liked = LikeAlbum.objects.get(album=album, user=request.user)
            if liked:
                liked.delete()
                return redirect('beat:detail', album.id)
        except Exception:
            like = LikeAlbum.objects.create(album=album, user=request.user)
            like.save()
            user = request.user
            subject = user.username, "liked your Album - ", album.title
            text = "Hello " + user.first_name + ", \n\nThank you for joining us.\nYour Beginner's Beat account has been successfully created. \n\nListen to the music of beginner's (maybe the future composers/artists) and enjoy it."
            me = settings.EMAIL_HOST_USER
            send_mail(subject, text, me, [album.author.email,], fail_silently=True)
            return redirect('beat:detail', album.id)

@login_required(login_url="beat:login")
def like_music(request, music_id):
    if request.method == "POST":
        #music = Music.objects.get(pk=music_id)
        music = get_object_or_404(Music, pk=music_id)
        try:
            liked = LikeMusic.objects.get(music=music, user=request.user)
            if liked:
                liked.delete()
                return redirect('beat:detail-music', music.id)
        except Exception:
            like = LikeMusic.objects.create(music=music, user=request.user)
            like.save()
            return redirect('beat:detail-music', music.id)

@login_required(login_url="beat:login")
def like_video(request, video_id):
    if request.method == "POST":
        #video = Video.objects.get(pk=video_id)
        video = get_object_or_404(Video, pk=video_id)
        video.views -= 1
        video.save()
        try:
            liked = LikeVideo.objects.get(video=video, user=request.user)
            if liked:
                liked.delete()
                return redirect('beat:detail-video', video.id)
        except Exception:
            like = LikeVideo.objects.create(video=video, user=request.user)
            like.save()
            return redirect('beat:detail-video', video.id)

@login_required(login_url="beat:login")
def comment_album(request, album_id):
    #album = Album.objects.get(pk=album_id)
    album = get_object_or_404(Album, pk=album_id)
    if request.method == "GET":
        text = request.GET.get('comment_album')
        #if text == "":
        #    return redirect('beat:detail', album.id)
        comment = CommentAlbum.objects.create(user=request.user, album=album, text=text)
        comment.save()
        messages.success(request, "Comment Added Successfully!")
        return redirect('beat:detail', album.id)

@login_required(login_url="beat:login")
def comment_music(request, music_id):
    #music = Music.objects.get(pk=music_id)
    music = get_object_or_404(Music, pk=music_id)
    if request.method == "GET":
        text = request.GET.get('comment_music')
        if text == "":
            return redirect('beat:edit-album', music.id)
        comment = CommentMusic.objects.create(user=request.user, music=music, text=text)
        comment.save()
        messages.success(request, "Comment Added Successfully!")
        return redirect('beat:detail-music', music.id)

@login_required(login_url="beat:login")
def comment_video(request, video_id):
    #video = Video.objects.get(pk=video_id)
    video = get_object_or_404(Video, pk=video_id)
    video.views -= 1
    video.save()
    if request.method == "GET":
        text = request.GET.get('comment_video')
        if text == "":
            return redirect('beat:detail-video', video.id)
        comment = CommentVideo.objects.create(user=request.user, video=video, text=text)
        comment.save()
        messages.success(request, "Comment Added Successfully!")
        return redirect('beat:detail-video', video.id)

@login_required(login_url="beat:login")
def delete_comment_album(request, comment_id, album_id):
    if request.method == "POST":
        #comment = CommentAlbum.objects.get(pk=comment_id)
        comment = get_object_or_404(CommentAlbum, pk=comment_id)
        if comment.user == request.user or comment.album.author == request.user:
            comment.delete()
            return redirect('beat:detail', album_id)

@login_required(login_url="beat:login")
def delete_comment_music(request, comment_id, music_id):
    if request.method == "POST":
        #comment = CommentMusic.objects.get(pk=comment_id)
        comment = get_object_or_404(CommentMusic, pk=comment_id)
        if comment.user == request.user:
            comment.delete()
            return redirect('beat:detail-music', music_id)

@login_required(login_url="beat:login")
def delete_comment_video(request, video_id, comment_id):
    if request.method == "POST":
        comment = CommentVideo.objects.get(pk=comment_id)
        #comment = get_object_or_404(CommentVideo, pk=comment_id)
        #video = Video.objects.get(pk=video_id)
        video = get_object_or_404(Video, pk=video_id)
        video.views -= 1
        video.save()
        if comment.user == request.user or video.author == request.user:
            comment.delete()
            return redirect('beat:detail-video', video_id)

def search(request):
    if request.method == "GET":
        text = request.GET.get('search_text')
        if text == "":
            return redirect('beat:index')
        users = User.objects.filter(username__contains=text).order_by('?')
        albums = Album.objects.filter(title__contains=text).order_by('?')
        musics = Music.objects.filter(title__contains=text).order_by('?')
        return render(request, 'beat/index.html', {
            'albums': albums,
            'users': users,
            'musics': musics,
            'search_text': text,
        })

def about(request):
    return render(request, 'beat/about.html', {})

def liked_by_album(request, album_id):
    album = Album.objects.get(pk=album_id)
    likes = LikeAlbum.objects.filter(album=album)
    return render(request, 'beat/liked_by.html', {'likes': likes})

def liked_by_video(request, video_id):
    video = Video.objects.get(pk=video_id)
    likes = LikeVideo.objects.filter(video=video)
    return render(request, 'beat/liked_by.html', {'likes': likes})
