from rest_framework.test import APIClient
from django.contrib.auth.models import User

from testing.testcases import TestCase

LOGIN_URL = '/api/accounts/login/'
LOGOUT_URL = '/api/accounts/logout/'
SIGNUP_URL = '/api/accounts/signup/'
LOGIN_STATUS_URL = '/api/accounts/login_status/'

TEST_USERNAME = 'admin_account'
TEST_EMAIL = 'admin_test@minenails.com'
TEST_PASSWORD = 'admin_test_pwd'

class AccountTest(TestCase):

    def setUp(self):
        self.client = self.anonymous_client
        self.create_user(TEST_USERNAME, TEST_EMAIL, TEST_PASSWORD)

    def _test_success_logged_in(self, data):
        response = self.client.get(LOGIN_STATUS_URL)
        self.assertEqual(response.data['has_logged_in'], False)

        response = self.client.post(LOGIN_URL, data)
        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(response.data['user'], None)
        self.assertEqual(response.data['user']['username'], TEST_USERNAME)
        self.assertEqual(response.data['user']['email'], TEST_EMAIL)

        response = self.client.get(LOGIN_STATUS_URL)
        self.assertEqual(response.data['has_logged_in'], True)

    def test_login_case(self):
        # wrong http method
        data = {'username': TEST_USERNAME, 'password': TEST_PASSWORD}
        response = self.client.get(LOGIN_URL, data)
        self.assertEqual(response.status_code, 405)

        # missing password in request data
        data = {'username': TEST_USERNAME}
        response = self.client.post(LOGIN_URL, data)
        self.assertEqual(response.data['success'], False)

        # missing username in request data
        data = {'password': TEST_PASSWORD}
        response = self.client.post(LOGIN_URL, data)
        self.assertEqual(response.data['success'], False)

        # default login status
        response = self.client.get(LOGIN_STATUS_URL)
        self.assertEqual(response.data['has_logged_in'], False)

        # test wrong password
        data = {'username': TEST_USERNAME, 'password': "wrong_password", }
        response = self.client.post(LOGIN_URL, data)
        self.assertEqual(response.status_code, 400)

        # test wrong username (user doesn't exist)
        data = {'username': 'not_exist_user', 'password': 'not_exist_user123'}
        response = self.client.post(LOGIN_URL, data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['success'], False)
        self.assertEqual(response.data['message'], 'Please check input.')
        self.assertEqual(response.data['errors']['username'][0].__str__(), 'User does not exist.')

        # test wrong password (password doesn't match)
        data = {'username': TEST_USERNAME, 'password': "wrong_password"}
        response = self.client.post(LOGIN_URL, data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['success'], False)

        # test correct login situation
        data = {'username': TEST_USERNAME, 'password': TEST_PASSWORD}
        self._test_success_logged_in(data)

    def test_case_insensitive(self):
        data = {'username': TEST_USERNAME.upper(), 'password': TEST_PASSWORD}
        self._test_success_logged_in(data)

    def test_signup_case(self):

        # test_wrong_HTTP_method(self):
        data = {
            'email': TEST_EMAIL,
            'username': TEST_USERNAME,
            'password': TEST_PASSWORD,
        }
        response = self.client.get(SIGNUP_URL, data)
        self.assertEqual(response.status_code, 405)

        # missing username
        data = {
            'email': TEST_EMAIL,
            'password': TEST_PASSWORD,
        }
        response = self.client.post(SIGNUP_URL, data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['success'], False)

        # missing email
        data = {
            'username': TEST_USERNAME,
            'password': TEST_PASSWORD,
        }
        response = self.client.post(SIGNUP_URL, data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['success'], False)

        # missing password
        data = {
            'email': TEST_EMAIL,
            'username': TEST_USERNAME,
        }
        response = self.client.post(SIGNUP_URL, data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['success'], False)


        # not valid username: too short < 8, too long > 30, space, start with _
        username_poll = ['aa', '_aaaaaaaa', 'abcdefghijklmnopqrstuvwxyzabcdefghijk', 'sdad dsad']
        for username in username_poll:
            data = {
                'email': TEST_EMAIL,
                'username': username,
                'password': TEST_PASSWORD,
            }
            response = self.client.post(SIGNUP_URL, data)
            self.assertEqual(response.status_code, 400)
            self.assertEqual(response.data['success'], False)

        # username occupied
        data = {
            'username': TEST_USERNAME,
            'email': "random@minenails.com",
            'password': TEST_PASSWORD,
        }

        response = self.client.post(SIGNUP_URL, data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual('username' in response.data['errors'], True)
        self.assertEqual('email' in response.data['errors'], False)
        self.assertEqual(response.data['errors']['username'][0].__str__(), "This username has been occupied.")

        # email occupied
        data = {
            'username': 'random_account',
            'email': TEST_EMAIL,
            'password': TEST_PASSWORD,
        }
        response = self.client.post(SIGNUP_URL, data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual('email' in response.data['errors'], True)
        self.assertEqual('username' in response.data['errors'], False)
        self.assertEqual(response.data['errors']['email'][0].__str__(), "This email has been occupied.")

        # correct signup
        data = {
            'email': "new_email@minenails.com",
            'username': "new_account",
            'password': "newpassword",
        }
        response = self.client.post(SIGNUP_URL, data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['user']['username'], data['username'])
        self.assertEqual(response.data['user']['email'], data['email'])

        # default state -> logged in
        response = self.client.get(LOGIN_STATUS_URL)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['has_logged_in'], True)

    def test_logged_in_status(self):
        data = {
            'username': TEST_USERNAME,
            'password': TEST_PASSWORD,
        }
        response = self.client.post(LOGIN_URL, data)
        self.assertEqual(response.status_code, 200)
        response = self.client.get(LOGIN_STATUS_URL)
        self.assertEqual(response.data['has_logged_in'], True)

    def test_logged_out_status(self):
        response = self.client.get(LOGIN_STATUS_URL)
        self.assertEqual(response.data['has_logged_in'], False)

    def test_logout(self):
        response = self.client.get(LOGIN_STATUS_URL)
        self.assertEqual(response.data['has_logged_in'], False)

        data = {
            'email': TEST_EMAIL,
            'username': TEST_USERNAME,
            'password': TEST_PASSWORD,
        }

        response = self.client.post(LOGIN_URL, data)
        self.assertEqual(response.status_code, 200)

        response = self.client.post(LOGOUT_URL)
        self.assertEqual(response.status_code, 200)

