from django.urls import path

from . views import (LoginView, RegisterView, profile_view, 
    logout_view, settings_view)

urlpatterns = [
    path('login/', LoginView.as_view(redirect_authenticated_user=True), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('profile/', profile_view, name='profile'),
    path('logout/', logout_view, name='logout'),
    path('settings/', settings_view, name='settings'),
]
