from unittest.mock import Mock

from apps.users.factories import UserFactory
from django.contrib.auth.models import AnonymousUser
from django.test import TestCase
from rest_framework.views import APIView

from sparkplug_notifications.factories import NotificationFactory
from sparkplug_notifications.permissions import IsRecipient

from ..utils import create_partition_for_today


class TestIsRecipient(TestCase):
    def setUp(self):
        # Create a partition for the current date
        create_partition_for_today()

        self.user = UserFactory()
        self.other_user = UserFactory()
        self.notification = NotificationFactory(recipient=self.user)
        self.permission = IsRecipient()

    def test_has_object_permission_true(self):
        # User is the recipient of the notification
        request = Mock(user=self.user)
        view = Mock(spec=APIView)
        assert (
            self.permission.has_object_permission(
                request, view, self.notification
            )
            is True
        )

    def test_has_object_permission_false(self):
        # User is not the recipient of the notification
        request = Mock(user=self.other_user)
        view = Mock(spec=APIView)
        assert (
            self.permission.has_object_permission(
                request, view, self.notification
            )
            is False
        )

    def test_has_object_permission_anonymous_user(self):
        # Anonymous user cannot be the recipient
        anonymous_user = AnonymousUser()
        request = Mock(user=anonymous_user)
        view = Mock(spec=APIView)
        assert (
            self.permission.has_object_permission(
                request, view, self.notification
            )
            is False
        )
