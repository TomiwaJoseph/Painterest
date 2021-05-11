from django.urls import path, include
from . import views

urlpatterns = [
    # path('', views.index, name='index'),
    path('', views.IndexListView.as_view(), name='index'),
    path('notifications/', views.notifications, name='notifications'),
    path('messages/', views.view_messages, name='messages'),
    path('delete_message/<int:message_id>/', views.delete_message, name='delete_message'),
    path('view_message/<int:message_id>/', views.show_message, name='show_message'),
    path('paint/', views.paint, name='paint'),
    path('contact/', views.contact, name='contact'),
    path('about/', views.about, name='about'),
    path('add_comment/', views.add_comment, name='add_comment'),
    path('add_paint/', views.AddPaintingView.as_view(), name='add_paint'),
    path('add_paint_try/<int:painting_id>/', views.add_paint_try, name='add_paint_try'),
    path('view_paint/<int:pk>/<slug:paint>/', views.PaintingDetailView.as_view(), name='view_paint'),
]
