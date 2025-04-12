from dataclasses import dataclass

from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_dataclasses.serializers import DataclassSerializer
from sparkplug_core.utils import get_validated_dataclass

from ..models import Notification
from ..permissions import IsRecipient


@dataclass
class InputData:
    is_starred: bool


class SetStarView(APIView):
    """Sets the `is_starred` field for a notification."""

    permission_classes = (IsRecipient,)

    class InputSerializer(DataclassSerializer):
        class Meta:
            dataclass = InputData

    def patch(self, request: Request, uuid: str) -> Response:
        notification = get_object_or_404(Notification, uuid=uuid)

        self.check_object_permissions(request, notification)

        validated_data: InputData = get_validated_dataclass(
            self.InputSerializer,
            input_data=request.data,
        )

        notification.is_starred = validated_data.is_starred
        notification.save()

        return Response(status=status.HTTP_204_NO_CONTENT)
