from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.conf import settings
from PIL import Image

alphanumeric = RegexValidator(r'^[0-9a-zA-Z]*$', 'Only alphanumeric characters are allowed.')

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True, max_length=60)
    username = models.CharField(max_length=50, unique=True, validators=[alphanumeric])

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.username


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='profile', on_delete=models.CASCADE)
    image = models.ImageField(default='dp.jpg', upload_to='profile_pics')
    about = models.TextField(default='Write a little bit about yourself here', blank=True)
    website_url = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"

    def save(self, *args, **kwargs):
        super(Profile, self).save(*args, **kwargs)

        img = Image.open(self.image.path)
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)


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