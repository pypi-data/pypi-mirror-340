from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from sparkplug_core.permissions import IsAuthenticated

from ..queries import unread_count


class UnreadCountView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request: Request) -> Response:
        """Get the user's unread notifications count."""
        return Response(
            status=status.HTTP_200_OK,
            data=unread_count(request.user),
        )
