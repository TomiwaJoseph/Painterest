from django.db.models.signals import post_save
from django.conf import settings
from django.dispatch import receiver
from .models import Category, Profile

all_category = [obj for obj in Category.objects.all()]


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def save_profile(sender, instance, **kwargs):
    for i in range(len(all_category)):
        instance.profile.feed_tuner.add(all_category[i])
    instance.profile.save()
