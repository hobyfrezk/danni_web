# permission checks
# List all checkouts
# List checkouts for a customer
# List checkouts from a staff
# Create a Spending checkout, check customer balance
# Create a Recharge checkout, check customer balance
# Create a S/R checkout, check customer balance
# Delete a checkout, check customer balance (soft deletion)

from testing.testcases import TestCase
from checkouts.models import Checkout
from customers.models import Customer
from decimal import Decimal

CHECKOUTS_URL = '/api/checkouts/'
CHECKOUTS_FOR_CUSTOMER = '/api/customers/{}/checkouts/'
CHECKOUTS_FOR_STAFF = '/api/employees/{}/checkouts/'
CHECKOUTS_DELETE = '/api/checkouts/{}/delete/'

class CheckoutsTest(TestCase):

    def setUp(self):
        """
        initialize_testing_accounts()
            - self.anonymous_client,
            - self.registered_client,
            - self.registered_client2,
            - self.staff_client,
            - self.admin_client,

        initialize_categories() & self.initialize_products()
            - self.category_1,
                - self.product_1
                - self.product_2
            - self.category_2,
            - self.category_3,

        initialize_appointments()
            - self.appointment_1: one hour later,
            - self.appointment_2: appointment yesterday
            - self.appointment_3: appointment ongoing
        """
        self.initialize_account()
        self.initialize_categories()
        self.initialize_products()
        self.initialize_appointments()

        self.checkout_1 = Checkout.objects.create(
            user=self.registered_user,
            appointment=self.appointment_2,
            served_by=self.staff_user.staff,
            checked_by=self.staff_user.staff,
            type=0,
            amount=50,
            pst=0.06,
            gst=0.07,
            checkout_snapshot="test checkout 1"
        )
        self.checkout_1.products.add(self.product_1, self.product_2)

        self.checkout_2 = Checkout.objects.create(
            user=self.registered_user,
            served_by=self.staff_user.staff,
            checked_by=self.staff_user.staff,
            type=0,
            amount=60,
            pst=0.06,
            gst=0.07,
            checkout_snapshot="test checkout 2"
        )
        self.checkout_2.products.add(self.product_1)
        
        self.checkout_3 = Checkout.objects.create(
            user=self.registered_user2,
            served_by=self.admin_user.staff,
            checked_by=self.admin_user.staff,
            type=1,
            amount=100,
            pst=0.06,
            gst=0.07,
            checkout_snapshot="test checkout 3"
        )
        
    def test_model(self):
        self.assertEquals(Checkout.objects.count(), 3)
    
    def test_list_checkouts(self):
        for client in [self.anonymous_client, self.registered_client, self.registered_client2]:
            response = client.get(CHECKOUTS_URL)
            self.assertEqual(response.status_code, 403)


        for client in [self.admin_client, self.staff_client]:
            response = client.get(CHECKOUTS_URL)
            checkouts = response.data.get("data")
            self.assertEqual(response.status_code, 200)
            self.assertEquals(len(checkouts), 3)
            self.assertEquals(checkouts[0]["id"], self.checkout_1.id)
            self.assertEquals(checkouts[1]["id"], self.checkout_2.id)
            self.assertEquals(checkouts[2]["id"], self.checkout_3.id)


    def test_retrieve_for_customer(self):
        url = CHECKOUTS_FOR_CUSTOMER.format(self.registered_user.customer.id)

        for client in [self.anonymous_client, self.registered_client2]:
            response = client.get(url)
            self.assertEqual(response.status_code, 403)

        for client in [self.admin_client, self.staff_client, self.registered_client]:
            response = client.get(url)
            self.assertEqual(response.status_code, 200)
            checkouts = response.data.get("data")
            self.assertEquals(len(checkouts), 2)


    def test_retrieve_for_employees(self):
        url = CHECKOUTS_FOR_STAFF.format(self.staff_user.staff.id)
        for client in [self.anonymous_client, self.registered_client, self.registered_client2]:
            response = client.get(url)
            self.assertEqual(response.status_code, 403)

        for client in [self.admin_client, self.staff_client]:
            response = client.get(url)
            checkouts = response.data.get("data")
            self.assertEqual(response.status_code, 200)
            self.assertEquals(len(checkouts), 2)

        url = CHECKOUTS_FOR_STAFF.format(self.admin_user.staff.id)
        for client in [self.admin_client, self.staff_client]:
            response = client.get(url)
            checkouts = response.data.get("data")
            self.assertEqual(response.status_code, 200)
            self.assertEquals(len(checkouts), 1)

    def test_create_spending_checkouts(self):
        data_spending = {
            "user": self.registered_user.id,
            "appointment": self.appointment_2.id,
            "served_by": self.admin_user.staff.id,
            "products": [self.product_1.id, self.product_2.id],
            "type": 0,
            "amount": 50,
            "gst": 0.07,
            "pst": 0.05,
            "checkout_snapshot": "test_checkout_1",
            "notes": "",
        }

        data_recharge = {
            "user": self.registered_user.id,
            "type": 1,
            "amount": 100,
            "checkout_snapshot": "recharge",
            "gst": 0.07,
            "pst": 0.05,
            "notes": "",
        }

        for client in [self.anonymous_client, self.registered_client, self.registered_client2]:
            response = client.post(CHECKOUTS_URL, data_spending)
            self.assertEqual(response.status_code, 403)

        # over spending -> 400
        n_checkouts = Checkout.objects.count()
        response = self.admin_client.post(CHECKOUTS_URL, data_spending)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(Checkout.objects.count() - n_checkouts, 0)

        # recharging -> 201
        for client in [self.admin_client, self.staff_client]:
            n_checkouts = Checkout.objects.count()
            balance_before = Customer.objects.get(id=self.registered_user.customer.id).balance
            response = client.post(CHECKOUTS_URL, data_recharge)
            balance_after = Customer.objects.get(id=self.registered_user.customer.id).balance
            self.assertEqual(response.status_code, 201)
            self.assertEqual(Checkout.objects.count() - n_checkouts, 1)
            self.assertEqual(balance_after - balance_before, 100)


        for client in [self.admin_client, self.staff_client]:
            n_checkouts = Checkout.objects.count()
            balance_before = Customer.objects.get(id=self.registered_user.customer.id).balance
            total_amount = Decimal(data_spending["amount"] * (1 + data_spending["pst"] + data_spending["gst"])).quantize(Decimal('.01'))
            response = client.post(CHECKOUTS_URL, data_spending)
            balance_after = Customer.objects.get(id=self.registered_user.customer.id).balance

            self.assertEqual(response.status_code, 201)
            self.assertEqual(Checkout.objects.count() - n_checkouts, 1)
            self.assertEqual(balance_before - balance_after, total_amount)

    def test_cancel(self):
        for client, checkout in zip([self.anonymous_client, self.registered_client, self.registered_client2],
                                    [self.checkout_1, self.checkout_2, self.checkout_3]):
            url = CHECKOUTS_DELETE.format(checkout.id)
            response = client.post(url, {})
            self.assertEqual(response.status_code, 403)

        for client, checkout in zip([self.staff_client, self.admin_client, self.admin_client],
                                    [self.checkout_1, self.checkout_2, self.checkout_3]):

            balance_before = Customer.objects.get(user=checkout.user).balance
            url = CHECKOUTS_DELETE.format(checkout.id)
            response = client.post(url, {})
            balance_after = Customer.objects.get(user=checkout.user).balance
            self.assertEqual(response.status_code, 201)
            self.assertEqual(response.data["checkout"]["is_deleted"], True)
            self.assertNotEqual(balance_after, balance_before)
