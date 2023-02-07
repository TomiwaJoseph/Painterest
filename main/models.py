import os
from django.conf import settings
from uuid import uuid4
from django.urls import reverse
from taggit.managers import TaggableManager
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
import sys
from PIL import Image
from django.db import models


class Paintings(models.Model):
    adder = models.ForeignKey(settings.AUTH_USER_MODEL,
                              on_delete=models.CASCADE, related_name='painter')
    painting = models.ImageField(upload_to='paintings', blank=True)
    title = models.CharField(max_length=50, blank=False)
    slug = models.SlugField(max_length=50)
    artist_name = models.CharField(max_length=50, blank=True)
    date_painted = models.DateTimeField(auto_now_add=True, db_index=True)
    tags = TaggableManager()

    def __str__(self):
        return "{}'s {}".format(self.adder, self.title)

    class Meta:
        verbose_name_plural = 'Paintings'
        ordering = ('-date_painted',)

    def get_absolute_url(self):
        return reverse('view_paint', args=[self.pk, self.slug])

    def save(self, *args, **kwargs):
        img = Image.open(self.painting)
        output = BytesIO()

        current_file_ext = self.painting.name.split('.')[-1]
        ext = ''
        if current_file_ext == 'jpg' or current_file_ext == 'jfif':
            ext = 'JPEG'
        else:
            ext = current_file_ext

        img.save(output, format='{}'.format(ext).upper(), quality=100)
        output.seek(0)

        the_hex = uuid4().hex
        self.slug = the_hex
        self.painting = InMemoryUploadedFile(output, "ImageField",
                                             f'{the_hex}.jpg', 'image/jpeg',
                                             sys.getsizeof(output), None)

        super().save(*args, **kwargs)


class Message(models.Model):
    sender = models.ForeignKey(settings.AUTH_USER_MODEL,
                               on_delete=models.CASCADE, related_name='message_sender')
    recepient = models.ForeignKey(settings.AUTH_USER_MODEL,
                                  on_delete=models.CASCADE, related_name='message_recepient')
    subject = models.CharField(default='Some subject', max_length=100)
    message = models.TextField(blank=False)
    read = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True, db_index=True)

    def __str__(self):
        return '{} sent {} a message'.format(self.sender, self.recepient)

    class Meta:
        ordering = ('-timestamp',)


class Comment(models.Model):
    painting = models.ForeignKey(Paintings,
                                 on_delete=models.CASCADE, related_name='paint_comments')
    body = models.CharField(max_length=255)
    commenter = models.ForeignKey(settings.AUTH_USER_MODEL,
                                  on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{} commented on {}'.format(self.commenter, self.painting)


class PaintTries(models.Model):
    painting = models.ForeignKey(Paintings,
                                 on_delete=models.CASCADE, related_name='painted')
    tryer = models.ForeignKey(settings.AUTH_USER_MODEL,
                              on_delete=models.CASCADE)
    tries = models.ImageField(upload_to='painting-tries')
    slug = models.SlugField(default='slug', max_length=250)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{} tried {}'.format(self.tryer, self.painting)

    class Meta:
        verbose_name_plural = 'Paint Tries'
        verbose_name = 'Paint Try'
        ordering = ('-created',)

    def get_absolute_url(self):
        return reverse('view_paint', args=[self.pk, self.slug])

    def save(self, *args, **kwargs):
        super(PaintTries, self).save(*args, **kwargs)

        ext = self.tries.name.split('.')[-1]
        the_hex = uuid4().hex
        initial_path = self.tries.path
        new_path = settings.MEDIA_ROOT + \
            '\painting-tries\{}.{}'.format(the_hex, ext)
        os.rename(initial_path, new_path)
        self.tries = new_path
        self.slug = the_hex
        super(PaintTries, self).save(*args, **kwargs)


class Folder(models.Model):
    name = models.CharField(max_length=50, blank=False, unique=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             related_name='folder_owner', on_delete=models.CASCADE)
    saved_painting = models.ManyToManyField(
        Paintings, through="FolderMember", blank=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user}'s folder -> {self.name}"

    class Meta:
        ordering = ('-date_created',)


class FolderMember(models.Model):
    painting = models.ForeignKey(Paintings, on_delete=models.CASCADE)
    folder = models.ForeignKey(Folder, on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.painting.title}"

    class Meta:
        ordering = ('-date_added',)


# Delete paintings in db on delete
