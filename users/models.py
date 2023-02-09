from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.validators import RegexValidator
from django.conf import settings
from PIL import Image
from uuid import uuid4
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
import sys
from django.utils.text import slugify


alphanumeric = RegexValidator(
    r'^[0-9a-zA-Z]*$', 'Only alphanumeric characters are allowed.')


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True')
        return self._create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    """User model"""
    email = models.EmailField(
        verbose_name='email address',
        max_length=60,
        unique=True
    )
    username = models.CharField(
        max_length=50, unique=True, validators=[alphanumeric])

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.username


class Category(models.Model):
    name = models.CharField(max_length=100, blank=False)
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
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, related_name='profile', on_delete=models.CASCADE)
    image = models.ImageField(
        default='90a70ab564f045a48488cd440f3b56e4-dp.jpg', upload_to='profile_pics', blank=True)
    about = models.TextField(blank=True)
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
    user_from = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='rel_from_set', on_delete=models.CASCADE)
    user_to = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='rel_to_set', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True, db_index=True)
    following = models.ManyToManyField(
        'self',
        # through='UserFollowing',
        related_name='followers',
        symmetrical=False
    )

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return '{} follows {}'.format(self.user_from,
                                      self.user_to)


CustomUser.add_to_class('following',
                        models.ManyToManyField('self', through=UserFollowing,
                                               related_name='followers', symmetrical=False))
