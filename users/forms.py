from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model
from django import forms
from .models import Profile


class RegisterForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ('email', 'username', 'password1', 'password2')


class LoginForm(AuthenticationForm):
    username = forms.CharField(label='Email or Username')


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ('username',)


class ProfileUpdateForm(forms.ModelForm):
    image = forms.ImageField(required=False,
                             widget=forms.FileInput, error_messages={'invalid': ('Image files only')})

    class Meta:
        model = Profile
        fields = ('image', 'about', 'website_url')
        widgets = {
            'website_url': forms.TextInput(
                attrs={'placeholder': 'Write your website url here...'}),
        }
