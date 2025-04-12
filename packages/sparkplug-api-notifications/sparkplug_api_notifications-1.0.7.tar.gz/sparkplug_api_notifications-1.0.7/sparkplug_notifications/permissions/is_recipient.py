from rest_framework.request import Request
from rest_framework.views import APIView
from rules import test_rule
from sparkplug_core.permissions import IsAuthenticated


class IsRecipient(IsAuthenticated):
    def has_object_permission(
        self,
        request: Request,
        view: APIView,
        obj: object,
    ) -> bool:
        return test_rule("is_recipient", obj, request.user)
