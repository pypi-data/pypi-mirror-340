from unittest.mock import Mock

from django.contrib.auth import get_user_model
from django.test import TestCase

from sparkplug_core.permissions.rules import is_admin

User = get_user_model()


class TestIsAdmin(TestCase):
    def setUp(self):
        self.user = Mock(spec=User)

    def test_is_admin_true(self):
        self.user.is_authenticated = True
        self.user.is_active = True
        self.user.is_staff = True
        assert is_admin(self.user)

    def test_is_admin_false_not_authenticated(self):
        self.user.is_authenticated = False
        self.user.is_active = True
        self.user.is_staff = True
        assert not is_admin(self.user)

    def test_is_admin_false_not_active(self):
        self.user.is_authenticated = True
        self.user.is_active = False
        self.user.is_staff = True
        assert not is_admin(self.user)

    def test_is_admin_false_not_staff(self):
        self.user.is_authenticated = True
        self.user.is_active = True
        self.user.is_staff = False
        assert not is_admin(self.user)
