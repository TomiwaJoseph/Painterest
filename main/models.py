import os
from django.db import models
from django.conf import settings
from uuid import uuid4
from django.urls import reverse


class Paintings(models.Model):
    adder = models.ForeignKey(settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE, related_name='painter')
    painting = models.ImageField(upload_to='paintings')
    title = models.CharField(max_length=50, blank=True)
    feel = models.CharField(max_length=255, blank=True)
    slug = models.SlugField(default='slug', max_length=250)

    def __str__(self):
        return '{} added {}'.format(self.adder, self.title)
    
    class Meta:
        verbose_name_plural = 'Paintings'

    def get_absolute_url(self):
        return reverse('view_paint', args=[self.pk, self.slug])

    def save(self, *args, **kwargs):
        super(Paintings, self).save(*args, **kwargs)

        ext = self.painting.name.split('.')[-1]
        the_hex = uuid4().hex
        initial_path = self.painting.path
        new_path = settings.MEDIA_ROOT + '\paintings\{}.{}'.format(the_hex, ext)
        os.rename(initial_path, new_path)
        self.painting = new_path
        self.slug = the_hex
        super(Paintings, self).save(*args, **kwargs)



# class Comment(models.Model):
#     painting = models.ForeignKey(Paintings,
#         on_delete=models.CASCADE, related_name='paint')
#     body = models.CharField(max_length=255)
#     commenter = models.ForeignKey(settings.AUTH_USER_MODEL,
#         on_delete=models.CASCADE)
#     created = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return '{} commented on {}'.format(self.commenter, self.painting)


# class PaintTries(models.Model):
    # painting = models.ForeignKey(Paintings,
    #     on_delete=models.CASCADE, related_name='paint-try')
    # tryer = models.ForeignKey(settings.AUTH_USER_MODEL,
    #     on_delete=models.CASCADE)
    # tries = models.ImageField(upload_to='paint-tries')

    # def __str__(self):
    #     return '{} tried {}'.format(self.tryer, self.painting)

