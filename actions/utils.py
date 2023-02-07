import datetime
from django.utils import timezone
from .models import Action


def create_action(user, verb, target, action_for):
    now = timezone.now()
    last_minute = now - datetime.timedelta(minutes=60)

    if verb == 'started following':
        similar_actions = Action.objects.filter(user_id=user.id,
                                                action_for=action_for, created__gte=last_minute)
        if not similar_actions:
            action = Action(user=user, verb=verb,
                            target=target, action_for=action_for)
            action.save()
            return True
    else:
        action = Action(user=user, verb=verb, target=target,
                        action_for=action_for)
        action.save()
        return True
