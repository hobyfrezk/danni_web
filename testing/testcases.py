from django.contrib.auth.models import User
from django.test import TestCase as DjangoTestCase
from rest_framework.test import APIClient

from categories.models import Category
from products.models import Product

TEST_USERNAME = 'client_account'
TEST_EMAIL = 'client_test@minenails.com'
TEST_PASSWORD = 'client_test_pwd'

TEST_USERNAME_ADMIN = 'admin_account'
TEST_EMAIL_ADMIN = 'admin_test@minenails.com'
TEST_PASSWORD_ADMIN = 'admin_test_pwd'

TEST_USERNAME_STAFF = 'staff_account'
TEST_EMAIL_STAFF = 'staff_test@minenails.com'
TEST_PASSWORD_STAFF = 'staff_test_pwd'


class TestCase(DjangoTestCase):

    @staticmethod
    def _create_user(username, email, password, is_admin, is_staff):
        if is_admin:
            return User.objects.create_superuser(username, email, password)
        if is_staff:
            return User.objects.create_user(username, email, password, is_staff=is_staff)
        else:
            # not admin nor staff -> normal user
            return User.objects.create_user(username, email, password)

    def create_user(self, username=None, email=None, password=None, is_admin=False, is_staff=False):
        if username is None:
            username = TEST_USERNAME
        if password is None:
            password = TEST_PASSWORD
        if email is None:
            email = TEST_EMAIL

        return self._create_user(username, email, password, is_admin, is_staff)

    @property
    def anonymous_client(self):
        if hasattr(self, '_anonymous_client'):
            return self._anonymous_client
        self._anonymous_client = APIClient()
        return self._anonymous_client

    def create_and_authenticate_client(self,
                                       username=None,
                                       email=None,
                                       password=None,
                                       is_admin=False,
                                       is_staff=False):

        user = self.create_user(username, email, password, is_admin, is_staff)
        client = APIClient()
        client.force_authenticate(user)
        return [user, client]

    def create_product(self, name, price, category):
        return Product.objects.create(name=name, price=price, category_id=category.id)

    def initialize_account(self):
        # self.anonymous_client
        if hasattr(self, '_anonymous_client'):
            return self._anonymous_client

        self.registered_user, self.registered_client = self.create_and_authenticate_client(
            TEST_USERNAME,
            TEST_EMAIL,
            TEST_PASSWORD,
            is_admin=False
        )

        self.staff_user, self.staff_client = self.create_and_authenticate_client(
            TEST_USERNAME_STAFF,
            TEST_EMAIL_STAFF,
            TEST_PASSWORD_STAFF,
            is_admin=False,
            is_staff=True,
        )

        self.admin_user, self.admin_client = self.create_and_authenticate_client(
            TEST_USERNAME_ADMIN,
            TEST_EMAIL_ADMIN,
            TEST_PASSWORD_ADMIN,
            is_admin=True
        )

    def initialize_categories(self):
        self.category_1 = Category.objects.create(name='Manicure')
        self.category_2 = Category.objects.create(name='Pedicure')
        self.category_3 = Category.objects.create(name='Accessory')

    def initialize_products(self):
        self.product_1 = self.create_product(
            name="Spa Polish Manicure", price=25, category=self.category_1
        )

        self.product_2 = self.create_product(
            name="Spa Shellac Manicure", price=35, category=self.category_1
        )