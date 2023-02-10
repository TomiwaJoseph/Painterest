from actions.models import Action
from main.models import Message


def notify_user(request):
    if request.user.is_authenticated:
        return {
            'unread_count': Message.objects.filter(recepient=request.user, read=False).count(),
            'notify': len(Action.objects.filter(action_for=request.user, read=False))
        }
    return {
        'unread_count': 0,
        'notify': 0
    }
