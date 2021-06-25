from django.contrib.auth.models import User
from django.test import TestCase as DjangoTestCase
from rest_framework.test import APIClient

from products.models import Product

TEST_USERNAME = 'admin_account'
TEST_EMAIL = 'admin_test@minenails.com'
TEST_PASSWORD = 'admin_test_pwd'

class TestCase(DjangoTestCase):

    @staticmethod
    def _create_user(username, email, password, is_admin):
        if is_admin:
            return User.objects.create_superuser(username, email, password)
        else:
            return User.objects.create_user(username, email, password)

    def create_user(self, username=None, email=None, password=None, is_admin=None):
        if username is None:
            username = TEST_USERNAME
        if password is None:
            password = TEST_PASSWORD
        if email is None:
            email = TEST_EMAIL

        return self._create_user(username, email, password, is_admin)

    @property
    def anonymous_client(self):
        if hasattr(self, '_anonymous_client'):
            return self._anonymous_client
        self._anonymous_client = APIClient()
        return self._anonymous_client

    def create_and_authenticate_client(self, username=None, email=None, password=None, is_admin=False):
        user = self.create_user(username, email, password, is_admin)
        client = APIClient()
        client.force_authenticate(user)
        return client

    def create_product(self, name, price, category):
        return Product.objects.create(name=name, price=price,category_id=category.id)