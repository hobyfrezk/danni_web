from testing.testcases import TestCase
from django.contrib.auth.models import User

EMPLOYEE_URL = '/api/employees/'
EMPLOYEE_URL_DETAIL = '/api/employees/{}/'
EMPLOYEE_URL_ADD_SERVICES = '/api/employees/{}/add-services/'
EMPLOYEE_URL_REMOVE_SERVICES = '/api/employees/{}/remove-services/'
EMPLOYEE_APPOINTMENT_URL = '/api/employees/{}/appointments/'

class EmployeesApiTest(TestCase):
    def setUp(self):
        """
        initialize_testing_accounts
            - self.anonymous_client,
            - self.registered_client,
            - self.staff_client -> is_staff=True, is_superuser=False,
            - self.admin_client -> is_staff=True, is_superuser=True,

        initialize_categories and initialize_products
            - self.category_1,
                - self.product_1,
                - self.product_2,
            - self.category_2,
            - self.category_3,
        """

        self.initialize_account()
        self.initialize_categories()
        self.initialize_products()
        self.initialize_appointments()

        self.admin_user.staff.services.add(self.product_1.id, self.product_2.id)
        self.staff_user.staff.services.add(self.product_1.id)

    def test_list_employees(self):
        # list with anonymous client -> 200
        # list with logged-in client -> 200
        # list with staff client -> 200
        # list with admin client -> 200
        for client in [self.anonymous_client, self.registered_client, self.staff_client, self.admin_client]:
            response = client.get(EMPLOYEE_URL)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.data['success'], True)
            self.assertEqual(len(response.data['employees']), 2)

            self.assertEqual(response.data['employees'][0]['id'], self.staff_user.staff.id)
            self.assertEqual(response.data['employees'][1]['id'], self.admin_user.staff.id)

    def test_create_employee(self):
        # set self.registered_client as staff client
        data = {
            'user': self.registered_user.id,
            'services': [self.product_1.id],
            'nickname': "ergou"
        }

        # Insufficient permissions client post -> 403
        for client in [self.anonymous_client, self.registered_client, self.staff_client]:
            response = client.post(EMPLOYEE_URL, data=data)
            self.assertEqual(response.status_code, 403)

        # normal create post -> 201
        response = self.admin_client.post(EMPLOYEE_URL, data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["employee"]['user']['id'], self.registered_user.id)
        self.assertEqual(response.data["employee"]['user']['is_staff'], True)
        self.assertEqual(User.objects.get(pk=self.registered_user.id).is_staff, True)

        # wrong user_id given -> 400
        data = {
            'user': 9527,
            'services': [self.product_1.id],
            'nickname': "ergou"
        }
        response = self.admin_client.post(EMPLOYEE_URL, data)
        self.assertEqual(response.status_code, 400)

    def test_delete_employee(self):
        data = {
            'user': self.registered_user.id,
            'services': [self.product_1.id],
            'nickname': "ergou"
        }
        # normal create post -> 201
        response = self.admin_client.post(EMPLOYEE_URL, data)
        self.assertEqual(response.status_code, 201)
        employee_id = response.data['employee']['id']

        url = EMPLOYEE_URL_DETAIL.format(employee_id)
        # Insufficient permissions client post -> 403
        for client in [self.anonymous_client, self.registered_client, self.staff_client]:
            response = client.delete(url)
            self.assertEqual(response.status_code, 403)

        # normal delete post -> 200
        response = self.admin_client.delete(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(User.objects.get(pk=self.registered_user.id).is_staff, False)


    def test_update_services(self):
        data = {
            'user': self.registered_user.id,
            'services': [self.product_1.id],
            'nickname': "ergou"
        }
        # normal create post -> 201
        response = self.admin_client.post(EMPLOYEE_URL, data)
        self.assertEqual(response.status_code, 201)
        employee_id = response.data['employee']['id']

        url_add_services = EMPLOYEE_URL_ADD_SERVICES.format(employee_id)
        data = {
            'services': [self.product_2.id]
        }
        # add one service permission check -> 403
        for client in [self.anonymous_client, self.registered_client, self.staff_client]:
            response = client.post(url_add_services, data)
            self.assertEqual(response.status_code, 403)

        # add one service -> 201
        response = self.admin_client.post(url_add_services, data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["success"], True)
        self.assertEqual(len(response.data["employee"]["services"]), 2)
        self.assertEqual(response.data["employee"]["services"][0]["id"], self.product_1.id)
        self.assertEqual(response.data["employee"]["services"][1]["id"], self.product_2.id)

        # add duplicate service -> keep silent and return 201
        response = self.admin_client.post(url_add_services, data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["success"], True)
        self.assertEqual(len(response.data["employee"]["services"]), 2)
        self.assertEqual(response.data["employee"]["services"][0]["id"], self.product_1.id)
        self.assertEqual(response.data["employee"]["services"][1]["id"], self.product_2.id)

        # add more than one services ->  201
        self.product_3 = self.create_product(name="test3", price=25, category=self.category_1)
        self.product_4 = self.create_product(name="test4", price=25, category=self.category_1)
        data = {'services': [self.product_3.id, self.product_4.id]}

        response = self.admin_client.post(url_add_services, data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["success"], True)
        self.assertEqual(len(response.data["employee"]["services"]), 4)
        self.assertEqual(response.data["employee"]["services"][0]["id"], self.product_1.id)
        self.assertEqual(response.data["employee"]["services"][1]["id"], self.product_2.id)
        self.assertEqual(response.data["employee"]["services"][2]["id"], self.product_3.id)
        self.assertEqual(response.data["employee"]["services"][3]["id"], self.product_4.id)


        # add service not exist -> 400
        data = {'services': [self.product_2.id, 9527]}
        response = self.admin_client.post(url_add_services, data)
        self.assertEqual(response.status_code, 400)

        # delete one service
        data = {'services': [self.product_4.id]}
        url_remove_services = EMPLOYEE_URL_REMOVE_SERVICES.format(employee_id)
        response = self.admin_client.post(url_remove_services, data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["success"], True)
        self.assertEqual(len(response.data["employee"]["services"]), 3)
        self.assertEqual(response.data["employee"]["services"][0]["id"], self.product_1.id)
        self.assertEqual(response.data["employee"]["services"][1]["id"], self.product_2.id)
        self.assertEqual(response.data["employee"]["services"][2]["id"], self.product_3.id)


        # delete all services
        data = {'services': [self.product_3.id, self.product_1.id, self.product_2.id]}
        response = self.admin_client.post(url_remove_services, data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["success"], True)
        self.assertEqual(len(response.data["employee"]["services"]), 0)

    def test_list_appointments(self):
        url = EMPLOYEE_APPOINTMENT_URL.format(self.staff_user.staff.id)

        response = self.anonymous_client.get(url)
        self.assertEqual(response.status_code, 403)

        response = self.registered_client.get(url)
        self.assertEqual(response.status_code, 403)

        response = self.registered_client2.get(url)
        self.assertEqual(response.status_code, 403)

        response = self.staff_client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data["appointments"]), 3)

        response = self.admin_client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data["appointments"]), 3)
