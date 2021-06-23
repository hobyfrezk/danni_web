from django.contrib.auth.models import User
from django.test import TestCase as DjangoTestCase
from rest_framework.test import APIClient

TEST_USERNAME = 'admin_account'
TEST_EMAIL = 'admin_test@minenails.com'
TEST_PASSWORD = 'admin_test_pwd'

class TestCase(DjangoTestCase):

    @staticmethod
    def create_user(username=None, email=None, password=None):
        if username is None:
            username = TEST_USERNAME

        if password is None:
            password = TEST_PASSWORD

        if email is None:
            email = TEST_EMAIL

        return User.objects.create_user(username, email, password)

    @property
    def anonymous_client(self):
        if hasattr(self, '_anonymous_client'):
            return self._anonymous_client
        self._anonymous_client = APIClient()
        return self._anonymous_client


    def create_and_authenticate_client(self, username, email=None, password=None):
        user = self.create_user(username, email, password)
        client = APIClient()
        client.force_authenticate(user)
        return client