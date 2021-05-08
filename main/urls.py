from django.urls import path, include
from . import views

urlpatterns = [
    # path('', views.index, name='index'),
    path('notifications/', views.notifications, name='notifications'),
    path('messages/', views.view_messages, name='messages'),
    path('paint/', views.paint, name='paint'),
    path('', views.IndexListView.as_view(), name='index'),
    path('add_paint/', views.AddPaintingView.as_view(), name='add_paint'),
    path('view_paint/<int:pk>/<slug:paint>/', views.PaintingDetailView.as_view(), name='view_paint'),
]
