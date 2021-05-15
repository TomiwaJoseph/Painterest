from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.conf import settings
from PIL import Image
from uuid import uuid4
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
import sys
from django.utils.text import slugify


alphanumeric = RegexValidator(r'^[0-9a-zA-Z]*$', 'Only alphanumeric characters are allowed.')

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True, max_length=60)
    username = models.CharField(max_length=50, unique=True, validators=[alphanumeric])

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.username


class Category(models.Model):
    name = models.CharField(max_length=100, blank=True)
    slug = models.SlugField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Categories'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)

        super().save(*args, **kwargs)


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='profile', on_delete=models.CASCADE)
    image = models.ImageField(default='90a70ab564f045a48488cd440f3b56e4-dp.jpg', upload_to='profile_pics', blank=True)
    about = models.TextField(default='Write a little bit about yourself here', blank=True)
    website_url = models.CharField(max_length=50, blank=True)
    feed_tuner = models.ManyToManyField(Category, blank=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"

    def save(self, *args, **kwargs):
        img = Image.open(self.image)

        if img.height > 300 or img.width > 300:
            output = BytesIO()
            current_file_ext = self.image.name.split('.')[-1]
            ext = ''
            if current_file_ext == 'jpg' or current_file_ext == 'jfif':
                ext = 'JPEG'
            else:
                ext = current_file_ext
            img = img.resize((300, 300))

            img.save(output, format='{}'.format(ext).upper(), quality=100)
            output.seek(0)

            the_hex = uuid4().hex
            self.image = InMemoryUploadedFile(output, "ImageField",
                f'{the_hex}.jpg', 'image/jpeg',
                sys.getsizeof(output), None)

        super().save(*args, **kwargs)


class UserFollowing(models.Model):
    user_from = models.ForeignKey(settings.AUTH_USER_MODEL,
        related_name='rel_from_set',
        on_delete=models.CASCADE)
    user_to = models.ForeignKey(settings.AUTH_USER_MODEL,
        related_name='rel_to_set',
        on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True,
        db_index=True)
    following = models.ManyToManyField('self',
        through='UserFollowing',
        related_name='followers',
        symmetrical=False)

    class Meta:
        ordering = ('-created',)
        # constraints = [models.UniqueConstraint(fields=['user_from', 'user_to'], name='unique_followers')]
        # unique_together = [['user_from', 'user_to'],]
    
    def __str__(self):
        return '{} follows {}'.format(self.user_from,
            self.user_to)


CustomUser.add_to_class('following',
    models.ManyToManyField('self', through=UserFollowing,
    related_name='followers', symmetrical=False))