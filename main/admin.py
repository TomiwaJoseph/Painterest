from django.contrib import admin
from .models import (Paintings, Message, Comment,
                     PaintTries, Folder, FolderMember)

# Register your models here.
admin.site.register(Message)
admin.site.register(Comment)
admin.site.register(PaintTries)


class PaintingsAdmin(admin.ModelAdmin):
    list_display = ['adder', 'title', 'painting']
    prepopulated_fields = {'slug': ('title',)}


admin.site.register(Paintings, PaintingsAdmin)


class PaintInline(admin.TabularInline):
    model = FolderMember


class FolderAdmin(admin.ModelAdmin):
    inlines = [PaintInline,]


admin.site.register(Folder, FolderAdmin)
