from django.contrib import admin, messages
from .models import Action

# Register your models here.
class ActionAdmin(admin.ModelAdmin):
    list_display = ('user', 'verb', 'target', 'created', 'read')
    list_filter = ('created',)
    search_fields = ('verb',)

    def make_read(modeladmin, request, queryset):
        queryset.update(read=True)
        messages.success(request, 'Actions marked as read')

    def make_unread(modeladmin, request, queryset):
        queryset.update(read=False)
        messages.success(request, 'Actions marked as unread')

    admin.site.add_action(make_read, "Make Read")
    admin.site.add_action(make_unread, "Make Unread")

admin.site.register(Action, ActionAdmin)