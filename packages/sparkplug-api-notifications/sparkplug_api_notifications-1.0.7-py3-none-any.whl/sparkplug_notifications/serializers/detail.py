import importlib

from django.conf import settings
from rest_framework.serializers import ModelSerializer, SerializerMethodField

from ..models import Notification


def get_class(target: str):  # noqa: ANN201
    module_name, class_name = target.rsplit(".", 1)
    module = importlib.import_module(module_name)
    return getattr(module, class_name)


UserTeaser = get_class(settings.USER_TEASER)


class DetailSerializer(ModelSerializer):
    actor_uuid = SerializerMethodField()
    actor = UserTeaser()

    class Meta:
        model = Notification
        fields = (
            "uuid",
            "created",
            "actor_uuid",
            "actor",
            "actor_text",
            "has_read",
            "is_starred",
            "message",
            "target_route",
        )

    def get_actor_uuid(self, obj):
        """Retrieve the UUID of the actor."""
        return str(obj.actor.uuid) if obj.actor else None
