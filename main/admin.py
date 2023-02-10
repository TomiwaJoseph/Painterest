from django.contrib import admin
from .models import (Paintings, Message, Comment,
                     PaintTries, Folder, FolderMember)


admin.site.register(Comment)
admin.site.register(PaintTries)


class MessagesAdmin(admin.ModelAdmin):
    list_display = ['sender', 'recepient', 'read']
    list_editable = ['read']


class PaintingsAdmin(admin.ModelAdmin):
    list_display = ['adder', 'title', 'painting']
    prepopulated_fields = {'slug': ('title',)}


class PaintInline(admin.TabularInline):
    model = FolderMember


class FolderAdmin(admin.ModelAdmin):
    inlines = [PaintInline,]


admin.site.register(Message, MessagesAdmin)
admin.site.register(Paintings, PaintingsAdmin)
admin.site.register(Folder, FolderAdmin)
