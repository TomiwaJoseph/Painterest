from django.contrib import admin
from .models import Paintings, Message, Comment, PaintTries

# Register your models here.
admin.site.register(Paintings)
admin.site.register(Message)
admin.site.register(Comment)
admin.site.register(PaintTries)
