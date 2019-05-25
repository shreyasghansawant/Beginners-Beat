from django import forms
from .models import Album, Profile, Music, Video
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class SignUpForm(UserCreationForm):
    email = forms.EmailField(help_text="Please, Enter a Valid Email!", max_length=100)
    first_name = forms.CharField(help_text="Required. 30 characters or fewer.", max_length=30)
    last_name = forms.CharField(help_text="Required. 30 characters or fewer.", max_length=30)
    username = forms.CharField(help_text="Required. 30 characters or fewer. Letters, digits and @/./+/-/_ only. ", max_length=30)
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('dp', 'dob', 'bio')
        labels = {
            "dp": "Profile picture",
            "dob": "Date of birth",
            "bio": "Bio",
        }

class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')
        labels = {
            "username": "Username",
            "email": "Email",
            "first_name": "First name",
            "last_name": "Last name",
        }

class AlbumForm(forms.ModelForm):
    class Meta:
        model = Album
        fields = ('title', 'cover_dp', 'description')
        labels = {
            "title": "Title",
            "description": "Description",
            "cover_dp": "Cover picture",
        }

class MusicForm(forms.ModelForm):
    class Meta:
        model = Music
        fields = ('title', 'file')
        labels = {
            "title": "Title",
            "file": "Audio file",
        }

class VideoForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ('title', 'description', 'file', 'thumbnail')
        labels = {
            "title": "Title",
            "description": "Description",
            "file": "Video file",
            "thumbnail": "Thumbnail",
        }
