from datetime import datetime, timedelta

import pytz
from django.contrib.auth.models import User
from django.test import TestCase as DjangoTestCase
from rest_framework.test import APIClient

from appointments.models import Appointment
from categories.models import Category
from products.models import Product

TEST_USERNAME = 'client_account'
TEST_EMAIL = 'client_test@minenails.com'
TEST_PASSWORD = 'client_test_pwd'

TEST_USERNAME2 = 'client_account2'
TEST_EMAIL2 = 'client_test2@minenails.com'
TEST_PASSWORD2 = 'client_test_pwd2'

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
        # self.registered_user, self.registered_client
        # self.staff_user, self.staff_client
        # self.admin_user, self.admin_client

        self.registered_user, self.registered_client = self.create_and_authenticate_client(
            TEST_USERNAME,
            TEST_EMAIL,
            TEST_PASSWORD,
            is_admin=False,
            is_staff=False
        )
        self.registered_user.customer

        self.registered_user2, self.registered_client2 = self.create_and_authenticate_client(
            TEST_USERNAME2,
            TEST_EMAIL2,
            TEST_PASSWORD2,
            is_admin=False,
            is_staff=False
        )
        self.registered_user2.customer

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

    def initialize_appointments(self):
        # appointment one hour later
        self.appointment_1 = Appointment.objects.create(
            user_id=self.registered_user.id,
            appointment_time=datetime.now(pytz.utc) + timedelta(hours=1),
            duration=90,
            staff_id=self.staff_user.staff.id
        )
        self.appointment_1.services.add(self.product_1, self.product_2)

        # appointment yesterday
        self.appointment_2 = Appointment.objects.create(
            user_id=self.registered_user.id,
            appointment_time=(datetime.now(pytz.utc) - timedelta(hours=24)),
            duration=120,
            staff_id=self.staff_user.staff.id,
        )
        self.appointment_2.services.add(self.product_1)

        # appointment ongoing
        self.appointment_3 = Appointment.objects.create(
            user_id=self.registered_user.id,
            appointment_time=(datetime.now(pytz.utc) - timedelta(hours=1)),
            duration=120,
            staff_id=self.staff_user.staff.id,
        )
