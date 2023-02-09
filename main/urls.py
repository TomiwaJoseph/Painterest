from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('notifications/', views.notifications, name='notifications'),
    path('messages/', views.view_messages, name='view_messages'),
    path('send_message/', views.send_message, name='send_message'),
    path('delete_message/<int:message_id>/',
         views.delete_message, name='delete_message'),
    path('view_message/<int:message_id>/',
         views.show_message, name='show_message'),
    path('fetch_category/', views.category_fetch, name='fetch_category'),
    path('notifications/notification_fetch/',
         views.notification_fetch, name='notification_fetch'),
    path('view_paint/<int:pk>/<slug:paint>/similar_fetch/',
         views.similar_fetch, name='similar_fetch'),
    path('notifications/mark_single_as_read/',
         views.mark_single_as_read, name='mark_single_as_read'),
    path('notifications/mark_all_as_read/',
         views.mark_all_as_read, name='mark_all_as_read'),
    path('contact/', views.contact, name='contact'),
    path('about/', views.about, name='about'),
    path('add_comment/', views.add_comment, name='add_comment'),
    path('add_paint/', views.add_painting, name='add_paint'),
    path('add_paint_try/', views.add_paint_try, name='add_paint_try'),
    path('view_paint/<int:pk>/<slug:paint>/',
         views.PaintingDetailView.as_view(), name='view_paint'),
    path('save_to_folder/', views.save_to_folder, name='save_to_folder'),
    path('view_folders/', views.view_folders, name='view_folders'),
    path('delete_folder/<int:folder_pk>/',
         views.delete_folder, name='delete_folder'),
    path('delete_folder_paint/<int:folder_id>/<int:paint_pk>/',
         views.delete_folder_paint, name='delete_folder_paint'),
    path('folder_content/<int:folder>/',
         views.folder_content, name='folder_content'),
    path('download_painting/<int:paint_pk>/',
         views.download_painting, name='download_painting'),
    path('save_paint/<int:paint_pk>/', views.save_to_folder, name='save_paint'),
    path('create/', views.create_folder, name='create'),
]
