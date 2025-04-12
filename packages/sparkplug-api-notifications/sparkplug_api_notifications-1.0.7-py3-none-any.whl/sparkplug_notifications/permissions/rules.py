import rules
from django.contrib.auth.models import AbstractBaseUser

from sparkplug_notifications.models import Notification


@rules.predicate
def is_recipient(
    notification: Notification,
    user: AbstractBaseUser,
) -> bool:
    return notification.recipient == user


rules.add_rule("is_recipient", is_recipient)
