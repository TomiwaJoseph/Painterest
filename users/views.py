from django.contrib.auth import views as auth_views
from django.views import generic
from django.urls import reverse_lazy
from django.shortcuts import render, redirect

from .forms import LoginForm, RegisterForm, UserUpdateForm, ProfileUpdateForm
from django.contrib.auth import logout

# Create your views here.
class LoginView(auth_views.LoginView):
    form_class = LoginForm
    template_name = 'registration/login.html'


class RegisterView(generic.CreateView):
    form_class = RegisterForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('login')


def profile_view(request):
    return render(request, 'users/profile.html')

def logout_view(request):
    logout(request)
    return redirect('index')

def settings_view(request):
    if request.method == 'POST':
        user_update_form = UserUpdateForm(request.POST, instance=request.user)
        profile_update_form = ProfileUpdateForm(request.POST,
            request.FILES, instance=request.user.profile)
        if user_update_form.is_valid() and profile_update_form.is_valid():
            user_update_form.save()
            profile_update_form.save()
            return redirect('profile')
    else:
        user_update_form = UserUpdateForm(instance=request.user)
        profile_update_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'user_update_form': user_update_form,
        'profile_update_form': profile_update_form,
    }
    return render(request, 'users/settings.html', context)