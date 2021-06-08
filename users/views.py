from django.contrib.auth import views as auth_views
from django.views import generic
from django.urls import reverse_lazy
from django.shortcuts import render, redirect, get_object_or_404
from .forms import (LoginForm, RegisterForm, UserUpdateForm,
    ProfileUpdateForm)
from django.contrib.auth import logout
from .models import CustomUser, UserFollowing, Category, Profile
from django.contrib import messages
from main.models import Message, Paintings
import os, random
from django.conf import settings
from uuid import uuid4
from taggit.models import Tag
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from actions.models import Action
from actions.utils import create_action

# Create your views here.
def following_and_follower(request, painter):
    all_follower = UserFollowing.objects.filter(user_to=CustomUser.objects.filter(
        username=painter).first())
    all_following = UserFollowing.objects.filter(user_from=CustomUser.objects.filter(
        username=painter).first())

    follower_page = request.GET.get('page', 1)
    follower_paginator = Paginator(all_follower, 5)

    following_page = request.GET.get('page', 1)
    following_paginator = Paginator(all_following, 5)

    try:
        users_follower = follower_paginator.page(follower_page)
        users_following = following_paginator.page(following_page)
    except PageNotAnInteger:
        users_follower = follower_paginator.page(1)
        users_following = following_paginator.page(1)
    except EmptyPage:
        users_follower = follower_paginator.page(follower_paginator.num_pages)
        users_following = following_paginator.page(following_paginator.num_pages)

    context = {
        'followers_count': all_follower.count(),
        'following_count': all_following.count(),
        'users_follower': users_follower,
        'users_following': users_following,
    }
    if request.user.is_authenticated:
        context['notify'] = len(Action.objects.filter(user_id__in=request.user.following.values_list('id',
            flat=True), read=False))
        context['unread_count'] = Message.objects.filter(recepient=request.user, 
            read=False).count()

    return render(request, 'users/following_and_follower.html',context)

class MyLoginView(auth_views.LoginView):
    form_class = LoginForm
    template_name = 'registration/login.html'


class RegisterView(generic.CreateView):
    form_class = RegisterForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('login')


@login_required
def follow(request, to_follow):
    user_to_follow = CustomUser.objects.filter(username=to_follow).first()
    if request.user in user_to_follow.followers.all():
        messages.info(request, "You are already following this user.")
    elif request.user.username == to_follow:
        messages.info(request, "You can't follow yourself.")
    else:
        UserFollowing.objects.create(user_from=request.user, user_to=user_to_follow)
        create_action(request.user, 'started following', user_to_follow)
    
    return redirect('painter_profile', painter=to_follow)

@login_required
def unfollow(request, to_unfollow):
    user_to_unfollow = CustomUser.objects.filter(username=to_unfollow).first()
    if request.user.username == to_unfollow:
        messages.info(request, "You can't unfollow yourself.")
    elif request.user not in user_to_unfollow.followers.all():
        messages.info(request, "You are not following this user.")
    else:
        UserFollowing.objects.filter(user_from=request.user, user_to=user_to_unfollow).delete()
    
    return redirect('painter_profile', painter=to_unfollow)

@login_required
def profile_view(request):
    context = {
        'notify': len(Action.objects.filter(user_id__in=request.user.following.values_list('id',
            flat=True), read=False)),
        'unread_count': Message.objects.filter(recepient=request.user, 
            read=False).count()
    }
    return render(request, 'users/profile.html', context)

def painter_profile_view(request, painter):
    context = {
        'painter': CustomUser.objects.filter(username=painter).first(),
    }
    if request.user.is_authenticated:
        context['notify'] = len(Action.objects.filter(user_id__in=request.user.following.values_list('id',
            flat=True), read=False))
        context['unread_count'] = Message.objects.filter(recepient=request.user, 
            read=False).count()
    return render(request, 'users/painter_profile.html', context)

def logout_view(request):
    logout(request)
    return redirect('index')

@login_required
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

    all_categories = [i.slug for i in Category.objects.all()]
    picture_for_each_category = []
    for i in range(len(all_categories)):
        tagg = get_object_or_404(Tag, slug=all_categories[i])
        object_list = Paintings.objects.filter(tags__in=[tagg])
        urls = random.choice(object_list).painting.url
        picture_for_each_category.append(urls)

    user_categories = Profile.objects.get(user=request.user).feed_tuner.all()
    all_feed = [i.name for i in user_categories]
    
    context = {
        'notify': len(Action.objects.filter(user_id__in=request.user.following.values_list('id',
            flat=True), read=False)),
        'user_categories': user_categories,
        'cat_pictures': picture_for_each_category,
        'categories': Category.objects.all(),
        'cat_number': range(len(Category.objects.all())),
        'user_update_form': user_update_form,
        'profile_update_form': profile_update_form,
        'unread_count': Message.objects.filter(recepient=request.user, 
            read=False).count()
    }
    return render(request, 'users/settings.html', context)

@login_required
def feed_tuner(request):
    selected = request.POST.getlist('category')

    profile = Profile.objects.get(user=request.user)
    profile.feed_tuner.clear()

    profile_obj = Profile.objects.get(user=request.user)
    for option in selected:
        category_obj = Category.objects.get(name=option)
        profile_obj.feed_tuner.add(category_obj)

    return redirect('profile')
