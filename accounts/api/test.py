from django.test import TestCase
from rest_framework.test import APIClient
from django.contrib.auth.models import User

LOGIN_URL = '/api/accounts/login/'
LOGOUT_URL = '/api/accounts/logout/'
SIGNUP_URL = '/api/accounts/signup/'
LOGIN_STATUS_URL = '/api/accounts/login_status/'


class LoginAPITests(TestCase):

    @staticmethod
    def createUser(user_data):
        username = user_data['username']
        email = user_data['email']
        password = user_data['password']

        return User.objects.create_user(username, email, password)

    def _test_logged_in(self, data):
        response = self.client.get(LOGIN_STATUS_URL)
        self.assertEqual(response.data['has_logged_in'], False)

        response = self.client.post(LOGIN_URL, data)
        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(response.data['user'], None)
        self.assertEqual(response.data['user']['username'], self.test_data['username'])
        self.assertEqual(response.data['user']['email'], self.test_data['email'])

        response = self.client.get(LOGIN_STATUS_URL)
        self.assertEqual(response.data['has_logged_in'], True)

    def setUp(self):
        # will be called everytime test function is running
        self.client = APIClient()
        self.test_data = {
            'username': 'admin_account',
            'email': 'admin_test@minenails.com',
            'password': 'admin_test_pwd'
        }
        self.user = self.createUser(self.test_data)

    def test_wrong_case(self):
        # wrong http method
        data = {'username': self.test_data['username'], 'password': self.test_data['password']}
        response = self.client.get(LOGIN_URL, data)
        self.assertEqual(response.status_code, 405)

        # missing password in request data
        data = {'username': self.test_data['username']}
        response = self.client.post(LOGIN_URL, data)
        self.assertEqual(response.data['success'], False)

        # missing username in request data
        data = {'username': self.test_data['password']}
        response = self.client.post(LOGIN_URL, data)
        self.assertEqual(response.data['success'], False)

        # test default login status
        response = self.client.get(LOGIN_STATUS_URL)
        self.assertEqual(response.data['has_logged_in'], False)

        # test wrong password
        data = {'username': self.test_data['username'], 'password': "wrong_password", }
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
        data = {'username': self.test_data['username'], 'password': "wrong_password"}
        response = self.client.post(LOGIN_URL, data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['success'], False)
        self.assertEqual(response.data['message'], 'Username and password does not match.')

    def test_correct_login(self):
        data = {'username': self.test_data['username'], 'password': self.test_data['password'], }
        self._test_logged_in(data)

    def test_case_insensitive(self):
        data = {'username': self.test_data['username'].upper(), 'password': self.test_data['password']}
        self._test_logged_in(data)


class SignupAPITests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.test_data = {
            'username': 'admin_account',
            'email': 'admin_test@minenails.com',
            'password': 'admin_test_pwd'
        }

    def test_wrong_HTTP_method(self):
        response = self.client.get(SIGNUP_URL, self.test_data)
        self.assertEqual(response.status_code, 405)

    def test_missing_parameters(self):
        # missing username
        data = {'email': self.test_data['email'], 'password': self.test_data['password']}
        response = self.client.post(SIGNUP_URL, data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['success'], False)

        # missing email
        data = {'username': self.test_data['username'], 'password': self.test_data['password']}
        response = self.client.post(SIGNUP_URL, data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['success'], False)

        # missing password
        data = {'username': self.test_data['username'], 'email': self.test_data['email']}
        response = self.client.post(SIGNUP_URL, data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['success'], False)

    def test_not_valid_parameters(self):
        # not valid username: too short < 8, too long > 30, space, start with _

        username_poll = ['aa', '_aaaaaaaa', 'abcdefghijklmnopqrstuvwxyzabcdefghijk', 'sdad dsad']
        for username in username_poll:
            data = {'email': self.test_data['email'], 'username': username, 'password': self.test_data['password']}
            response = self.client.post(SIGNUP_URL, data)
            self.assertEqual(response.status_code, 400)
            self.assertEqual(response.data['success'], False)

        # email occupied
        username = self.test_data['username']
        email = "test_occupied@gmail.com"
        password = self.test_data['password']
        User.objects.create_user(username, email, password)

        response = self.client.post(SIGNUP_URL, self.test_data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual('username' in response.data['errors'], True)
        self.assertEqual('email' in response.data['errors'], False)
        self.assertEqual(response.data['errors']['username'][0].__str__(), "This username has been occupied.")

        # username occupied
        username = "username_occupied"
        email = self.test_data['email']
        password = self.test_data['password']
        User.objects.create_user(username, email, password)

        response = self.client.post(SIGNUP_URL, self.test_data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual('email' in response.data['errors'], True)
        self.assertEqual('username' in response.data['errors'], False)
        self.assertEqual(response.data['errors']['email'][0].__str__(), "This email has been occupied.")


    def test_signup_succeed(self):
        response = self.client.post(SIGNUP_URL, self.test_data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['user']['username'], self.test_data['username'])
        self.assertEqual(response.data['user']['email'], self.test_data['email'])

        response = self.client.get(LOGIN_STATUS_URL)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['has_logged_in'], True)


class LoginStatusAPITest(TestCase):
    @staticmethod
    def createUser(user_data):
        username = user_data['username']
        email = user_data['email']
        password = user_data['password']
        return User.objects.create_user(username, email, password)

    def setUp(self):
        self.client = APIClient()
        self.test_data = {
            'username': 'admin_account',
            'email': 'admin_test@minenails.com',
            'password': 'admin_test_pwd'
        }
        self.user = self.createUser(self.test_data)

    def test_logged_in_status(self):
        data = {'username': self.test_data['username'], 'password': self.test_data['password']}
        response = self.client.post(LOGIN_URL, data)
        self.assertEqual(response.status_code, 200)
        response = self.client.get(LOGIN_STATUS_URL)
        self.assertEqual(response.data['has_logged_in'], True)

    def test_logged_out_status(self):
        response = self.client.get(LOGIN_STATUS_URL)
        self.assertEqual(response.data['has_logged_in'], False)


class LogoutAPITest(TestCase):
    
    @staticmethod
    def createUser(user_data):
        username = user_data['username']
        email = user_data['email']
        password = user_data['password']
        return User.objects.create_user(username, email, password)
    
    def setUp(self):
        self.client = APIClient()
        self.test_data = {
            'username': 'admin_account',
            'email': 'admin_test@minenails.com',
            'password': 'admin_test_pwd'
        }
        self.user = self.createUser(self.test_data)

    def test_logout(self):
        response = self.client.get(LOGIN_STATUS_URL)
        self.assertEqual(response.data['has_logged_in'], False)

        response = self.client.post(LOGIN_URL, self.test_data)
        self.assertEqual(response.status_code, 200)

        response = self.client.post(LOGOUT_URL)
        self.assertEqual(response.status_code, 200)

