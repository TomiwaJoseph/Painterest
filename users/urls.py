from django.urls import path
from . import views 

urlpatterns = [
    path('login/', views.MyLoginView.as_view(redirect_authenticated_user=True), name='login'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile_view, name='profile'),
    path('painter_profile/<slug:painter>/', views.painter_profile_view, name='painter_profile'),
    path('<slug:painter>/following_and_follower/', views.following_and_follower, name='following_and_follower'),
    path('logout/', views.logout_view, name='logout'),
    path('follow/<slug:to_follow>/', views.follow, name='follow'),
    path('unfollow/<slug:to_unfollow>/', views.unfollow, name='unfollow'),
    path('settings/', views.settings_view, name='settings'),
    path('feed_tuner/', views.feed_tuner, name='feed_tuner'),
]
