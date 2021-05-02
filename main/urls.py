from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('notifications/', views.notifications, name='notifications'),
    path('messages/', views.messages, name='messages'),
]
