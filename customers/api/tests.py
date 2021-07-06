from rest_framework.test import APIClient

from customers.models import Customer
from testing.testcases import TestCase

SIGNUP_URL = '/api/accounts/signup/'
CUSTOMER_URL = '/api/customers/'
DETAIL_URL = '/api/customers/{}/'
UPDATE_PROFILE_URL = '/api/customers/{}/update-info/'
UPDATE_BALANCE_URL = '/api/customers/{}/update-balance/'
UPDATE_CUSTOMER_TIER_URL = '/api/customers/{}/update-tier/'

default_data_dict = {
    'username': 'customer_1',
    'password': 'customer_1_pwd',
    'email': 'customer_1@gmail.com',
}


class CustomerApiTests(TestCase):

    def setUp(self):
        self.initialize_account()

    def _check_success_signup(self, data):
        count_before = Customer.objects.count()
        response = self.anonymous_client.post(SIGNUP_URL, data)
        self.assertEqual(response.status_code, 201)

        count_after = Customer.objects.count()
        self.assertEqual(count_after - count_before, 1)

        self.assertEqual(response.data["user"]["username"], data['username'])
        self.assertEqual(response.data["user"]["profile"]['first_name'], data.get('first_name', ''))
        self.assertEqual(response.data["user"]["profile"]['last_name'], data.get('last_name', ''))
        self.assertEqual(response.data["user"]["profile"]['phone'], data.get('phone', ''))
        self.assertEqual(response.data["user"]["profile"]['gender'], data.get('gender', 0))
        self.assertEqual(response.data["user"]["profile"]['balance'], data.get('balance', '0.00'))

    def _check_success_update(self, owner_client, raw_data, url, user_id):

        data = {key: value + "1" for key, value in raw_data.items()}
        response = self.anonymous_client.post(url, data)
        self.assertEqual(response.status_code, 403)

        response = self.registered_client.post(url, data)
        self.assertEqual(response.status_code, 403)

        data = {key: value + "2" for key, value in raw_data.items()}
        response = owner_client.post(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["customer"]["user_id"], user_id)
        for key in raw_data:
            self.assertEqual(response.data["customer"][key], data[key])

        data = {key: value + "3" for key, value in raw_data.items()}
        response = self.staff_client.post(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["customer"]["user_id"], user_id)
        for key in raw_data:
            self.assertEqual(response.data["customer"][key], data[key])

        data = {key: value + "4" for key, value in raw_data.items()}
        response = self.admin_client.post(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["customer"]["user_id"], user_id)
        for key in raw_data:
            self.assertEqual(response.data["customer"][key], data[key])

    def test_create_customer(self):
        # create new account without give profile data -> 201
        data = default_data_dict
        self._check_success_signup(data)

        # create new account and give in-complete profile data
        data = {
            'username': 'customer_2',
            'password': 'customer_2_pwd',
            'email': 'customer_2@gmail.com',
            'gender': 1,
            'phone': '+14319548432',
        }
        self._check_success_signup(data)

        # wrong phone number -> 403 # TODO

        # correct create -> 201
        data = {
            'username': 'customer_3',
            'password': 'customer_3_pwd',
            'email': 'customer_3@gmail.com',
            'first_name': 'c3_first',
            'last_name': 'c3_last',
            'gender': 2,
            'phone': '+14319548432',
        }
        self._check_success_signup(data)

    def test_retrieve_customer_profile(self):
        data = default_data_dict
        client = APIClient()
        response = client.post(SIGNUP_URL, data)
        user_id = response.data["user"]["id"]
        profile_id = response.data["user"]["profile"]["id"]
        url = DETAIL_URL.format(profile_id)

        # abnormal retrieve -> 403
        response = self.anonymous_client.get(url)
        self.assertEqual(response.status_code, 403)

        # registered user retrieve -> 403
        response = self.registered_client.get(url)
        self.assertEqual(response.status_code, 403)

        # owner retrieve -> 200
        response = client.get(url)
        self.assertEqual(response.status_code, 200)

        # staff retrieve -> 200
        response = self.staff_client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["customer"]["user_id"], user_id)

        response = self.admin_client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["customer"]["user_id"], user_id)

    def test_update_customer_profile(self):

        # user doesnt exist -> 404

        data = default_data_dict
        client = APIClient()
        response = client.post(SIGNUP_URL, data)

        user_id = response.data["user"]["id"]
        profile_id = response.data["user"]["profile"]["id"]

        url = UPDATE_PROFILE_URL.format(profile_id)

        # update last_name -> 200
        data = {"last_name": "new_last_name"}
        self._check_success_update(client, data, url, user_id)

        # update first_name
        data = {"first_name": "new_first_name"}
        self._check_success_update(client, data, url, user_id)

        # update gender -> 200 TODO
        # wrong gender option -> 400 TODO
        # update wrong phone -> 403 TODO

        # update correct phone -> 200
        data = {"phone": "+11564532185"}
        self._check_success_update(client, data, url, user_id)

        # batch update -> 200
        data = {"first_name": "new_first_name", "phone": "+11564532185"}
        self._check_success_update(client, data, url, user_id)

    def test_update_customer_balance(self):
        # permission check
        # recharge update -> 200
        # spending update -> 200
        # TODO fanout to checkout table
        data = default_data_dict
        client = APIClient()
        response = client.post(SIGNUP_URL, data)
        profile_id = response.data["user"]["profile"]["id"]

        prev_balance = float(response.data["user"]["profile"]["balance"])

        url = UPDATE_BALANCE_URL.format(profile_id)

        data = {"balance": 50}

        # anonymous user post -> 403
        response = self.anonymous_client.post(url, data)
        self.assertEqual(response.status_code, 403)

        # other registered user post -> 403
        response = self.registered_client.post(url, data)
        self.assertEqual(response.status_code, 403)

        # owner user post -> 403
        response = client.post(url, data)
        self.assertEqual(response.status_code, 403)

        # staff post recharge -> 200
        response = self.staff_client.post(url, data)
        self.assertEqual(response.status_code, 200)
        after_balance = float(response.data['customer']["balance"])
        self.assertEqual(after_balance - prev_balance, 50)

        # admin post recharge -> 200
        prev_balance = after_balance
        response = self.staff_client.post(url, data)
        self.assertEqual(response.status_code, 200)
        after_balance = float(response.data['customer']["balance"])
        self.assertEqual(after_balance - prev_balance, 50)
        self.assertEqual(after_balance, 100)

        # staff post spending -> 200
        prev_balance = after_balance
        data = {"balance": -50}
        response = self.staff_client.post(url, data)
        self.assertEqual(response.status_code, 200)
        after_balance = float(response.data['customer']["balance"])
        self.assertEqual(after_balance - prev_balance, -50)

        # admin post spending -> 200
        prev_balance = after_balance
        response = self.staff_client.post(url, data)
        self.assertEqual(response.status_code, 200)
        after_balance = float(response.data['customer']["balance"])
        self.assertEqual(after_balance - prev_balance, -50)

    def test_update_customer_tier(self):
        # permission check
        data = default_data_dict
        client = APIClient()
        response = client.post(SIGNUP_URL, data)
        profile_id = response.data["user"]["profile"]["id"]

        tier = response.data["user"]["profile"]["tier"]
        url = UPDATE_CUSTOMER_TIER_URL.format(profile_id)

        data = {"tier": 1}

        # anonymous user post -> 403
        response = self.anonymous_client.post(url, data)
        self.assertEqual(response.status_code, 403)

        # other registered user post -> 403
        response = self.registered_client.post(url, data)
        self.assertEqual(response.status_code, 403)

        # owner user post -> 403
        response = client.post(url, data)
        self.assertEqual(response.status_code, 403)

        # staff post recharge -> 200
        response = self.staff_client.post(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['customer']['tier'], 1)

        # admin post recharge -> 200
        data = {"tier": 2}
        response = self.staff_client.post(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['customer']['tier'], 2)

        # wrong tier value
        data = {"tier": 5}
        response = self.staff_client.post(url, data)
        self.assertEqual(response.status_code, 400)
