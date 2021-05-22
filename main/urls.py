from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.IndexListView.as_view(), name='index'),
    path('notifications/', views.notifications, name='notifications'),
    path('messages/', views.view_messages, name='view_messages'),
    path('send_message/', views.send_message, name='send_message'),
    path('delete_message/<int:message_id>/', views.delete_message, name='delete_message'),
    path('view_message/<int:message_id>/', views.show_message, name='show_message'),
    path('paint/', views.paint, name='paint'),
    path('contact/', views.contact, name='contact'),
    path('about/', views.about, name='about'),
    path('add_comment/', views.add_comment, name='add_comment'),
    path('add_paint/', views.AddPaintingView.as_view(), name='add_paint'),
    path('add_paint_try/', views.add_paint_try, name='add_paint_try'),
    path('view_paint/<int:pk>/<slug:paint>/', views.PaintingDetailView.as_view(), name='view_paint'),
    path('save_to_folder/', views.save_to_folder, name='save_to_folder'),
    path('view_folders/', views.view_folders, name='view_folders'),
    path('delete_folder/<int:folder_pk>/', views.delete_folder, name='delete_folder'),
    path('delete_folder_paint/', views.delete_folder_paint, name='delete_folder_paint'),
    path('folder_content/<int:folder>/', views.folder_content, name='folder_content'),
    path('download_painting/<int:paint_pk>/', views.download_painting, name='download_painting'),
    path('save_paint/<int:paint_pk>/', views.save_to_folder, name='save_paint'),
    path('create/', views.create, name='create'),
]
