from django.db import models
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

# Create your models here.

class Action(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
        related_name='actions',
        db_index=True,
        on_delete=models.CASCADE)
    verb = models.CharField(max_length=255)
    target_ct = models.ForeignKey(ContentType,
        blank=True, related_name='target_obj',
        null=True, on_delete=models.CASCADE)
    target_id = models.PositiveIntegerField(null=True,
        blank=True, db_index=True)
    target = GenericForeignKey('target_ct', 'target_id')
    created = models.DateTimeField(auto_now_add=True,
        db_index=True)
    read = models.BooleanField(default=False)

    class Meta:
        ordering = ('-created',)