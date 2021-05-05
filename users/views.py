from django.contrib.auth import views as auth_views
from django.views import generic
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from .forms import LoginForm, RegisterForm, UserUpdateForm, ProfileUpdateForm
from django.contrib.auth import logout
from .models import CustomUser, UserFollowing
from django.contrib import messages


# Create your views here.
class LoginView(auth_views.LoginView):
    form_class = LoginForm
    template_name = 'registration/login.html'


class RegisterView(generic.CreateView):
    form_class = RegisterForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('login')


def following_and_follower(request, painter):
    return render(request, 'users/following_and_follower.html')

def follow(request, to_follow):
    user_to_follow = CustomUser.objects.filter(username=to_follow).first()
    if request.user in user_to_follow.followers.all():
        messages.info(request, "You are already following this user.")
        return redirect('painter_profile', painter=to_follow)
    elif request.user.username == to_follow:
        messages.info(request, "You can't follow yourself.")
        return redirect('painter_profile', painter=to_follow)
    else:
        UserFollowing.objects.create(user_from=request.user, user_to=user_to_follow)
    
    return redirect('painter_profile', painter=to_follow)

def unfollow(request, to_unfollow):
    user_to_unfollow = CustomUser.objects.filter(username=to_unfollow).first()
    if request.user.username == to_unfollow:
        messages.info(request, "You can't unfollow yourself.")
        return redirect('painter_profile', painter=to_unfollow)
    elif request.user not in user_to_unfollow.following.all():
        messages.info(request, "You are not following this user.")
        return redirect('painter_profile', painter=to_unfollow)
    else:
        UserFollowing.objects.delete(user_from=request.user, user_to=user_to_unfollow)
    
    return redirect('painter_profile', painter=to_unfollow)

def profile_view(request):
    return render(request, 'users/profile.html')

def painter_profile_view(request, painter):
    context = {
        'painter': CustomUser.objects.filter(username=painter).first()
    }
    return render(request, 'users/painter.html', context)

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