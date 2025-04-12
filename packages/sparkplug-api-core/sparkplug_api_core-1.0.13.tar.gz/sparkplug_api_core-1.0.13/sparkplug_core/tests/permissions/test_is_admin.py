from unittest.mock import Mock, patch

from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.request import Request
from rest_framework.views import APIView

from ...permissions import IsAdmin


@patch("sparkplug_core.permissions.is_admin.test_rule")
class TestIsAdmin(TestCase):
    def setUp(self):
        self.user = Mock(spec=User)
        self.request = Mock(spec=Request)
        self.view = Mock(spec=APIView)
        self.permission = IsAdmin()

    def test_has_permission_authenticated(self, mock_test_rule):
        mock_test_rule.return_value = True
        self.request.user = self.user

        result = self.permission.has_permission(self.request, self.view)

        mock_test_rule.assert_called_once_with("is_admin", self.user)
        assert result is True

    def test_has_permission_not_authenticated(self, mock_test_rule):
        mock_test_rule.return_value = False
        self.request.user = self.user

        result = self.permission.has_permission(self.request, self.view)

        mock_test_rule.assert_called_once_with("is_admin", self.user)
        assert result is False
