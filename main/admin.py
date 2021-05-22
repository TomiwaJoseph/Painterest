from django.contrib import admin
from .models import Paintings, Message, Comment, PaintTries, Folder

# Register your models here.
admin.site.register(Paintings)
admin.site.register(Message)
admin.site.register(Comment)
admin.site.register(PaintTries)
admin.site.register(Folder)

