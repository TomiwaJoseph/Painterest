from django.conf import settings


def notify_user(request):
    return {
        'email': settings.EMAIL_HOST_USER,
    }
