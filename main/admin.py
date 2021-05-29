from django.contrib import admin
from .models import (Paintings, Message, Comment, 
    PaintTries, Folder, FolderMember)

# Register your models here.
admin.site.register(Paintings)
admin.site.register(Message)
admin.site.register(Comment)
admin.site.register(PaintTries)

class PaintInline(admin.TabularInline):
    model = FolderMember

class FolderAdmin(admin.ModelAdmin):
    inlines = [
        PaintInline,
    ]

admin.site.register(Folder, FolderAdmin)