from django.urls import path

from . views import (LoginView, RegisterView, profile_view, 
    logout_view, settings_view, painter_profile_view, follow,
    unfollow, following_and_follower)

urlpatterns = [
    path('login/', LoginView.as_view(redirect_authenticated_user=True), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('profile/', profile_view, name='profile'),
    path('painter_profile/<slug:painter>/', painter_profile_view, name='painter_profile'),
    path('<slug:painter>/following_and_follower/', following_and_follower, name='following_and_follower'),
    path('logout/', logout_view, name='logout'),
    path('follow/<slug:to_follow>/', follow, name='follow'),
    path('unfollow/<slug:to_unfollow>/', unfollow, name='unfollow'),
    path('settings/', settings_view, name='settings'),
]
