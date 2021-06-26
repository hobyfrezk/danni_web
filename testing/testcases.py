from django.contrib.auth.models import User
from django.test import TestCase as DjangoTestCase
from rest_framework.test import APIClient

from products.models import Product
from categories.models import Category

TEST_USERNAME = 'client_account'
TEST_EMAIL = 'client_test@minenails.com'
TEST_PASSWORD = 'client_test_pwd'

TEST_USERNAME_ADMIN = 'admin_account'
TEST_EMAIL_ADMIN = 'admin_test@minenails.com'
TEST_PASSWORD_ADMIN = 'admin_test_pwd'



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

    def initialize_account(self):
        # self.anonymous_client
        self.registered_client = self.create_and_authenticate_client(
            TEST_USERNAME,
            TEST_EMAIL,
            TEST_PASSWORD,
            is_admin=False
        )
        self.admin_client = self.create_and_authenticate_client(
            TEST_USERNAME_ADMIN,
            TEST_EMAIL_ADMIN,
            TEST_PASSWORD_ADMIN,
            is_admin=True
        )

    def initialize_categories(self):
        self.category_1 = Category.objects.create(name='Manicure')
        self.category_2 = Category.objects.create(name='Pedicure')
        self.category_3 = Category.objects.create(name='Accessory')