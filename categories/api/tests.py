from categories.models import Category
from testing.testcases import TestCase


CATEGORY_URL = '/api/categories/'
CATEGORY_DETAIL_URL = '/api/categories/{}/'

TEST_USERNAME = 'client_account'
TEST_EMAIL = 'client_test@minenails.com'
TEST_PASSWORD = 'client_test_pwd'

TEST_USERNAME_ADMIN = 'admin_account'
TEST_EMAIL_ADMIN = 'admin_test@minenails.com'
TEST_PASSWORD_ADMIN = 'admin_test_pwd'



class CategoryApiTests(TestCase):
    def setUp(self):
        # self.client = self.anonymous_client
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
        
        self.category_1 = Category.objects.create(name='Manicure')
        self.category_2 = Category.objects.create(name='Pedicure')
        self.category_3 = Category.objects.create(name='Accessory')


    def test_list_categories(self):
        # list with anonymous client -> 200
        # list with logged-in client -> 200
        # list with admin client -> 200
        # returned categories in created_at order -> 200
        for client in [self.anonymous_client, self.registered_client, self.admin_client]:
            response = client.get(CATEGORY_URL)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(response.data['categories']), 3)

            self.assertEqual(response.data['categories'][0]['id'], self.category_1.id)
            self.assertEqual(response.data['categories'][1]['id'], self.category_2.id)
            self.assertEqual(response.data['categories'][2]['id'], self.category_3.id)


    def test_retrieve_category_with_detail(self):
        category_id = self.category_1.id
        url = CATEGORY_DETAIL_URL.format(category_id)

        self.create_product(name="Spa Polish Manicure", price=25, category=self.category_1)
        self.create_product(name="Spa Shellac Manicure", price=35, category=self.category_1)

        # list with anonymous client -> 200
        # list with logged-in client -> 200
        # list with admin client -> 200
        # returned categories in -created_at order -> 200
        for client in [self.anonymous_client, self.registered_client, self.admin_client]:
            response = client.get(url)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.data['data']['id'], category_id)
            self.assertEqual(len(response.data['data']['products']), 2)


    def test_create_category(self):
        # anonymous and registered client post -> 403
        data = {"name": "eyelash"}
        response = self.anonymous_client.post(CATEGORY_URL, data)
        self.assertEqual(response.status_code, 403)

        response = self.registered_client.post(CATEGORY_URL, data)
        self.assertEqual(response.status_code, 403)

        # admin client post empty -> 400
        response = self.admin_client.post(CATEGORY_URL, {})
        self.assertEqual(response.status_code, 400)

        # admin client post name -> 201
        response = self.admin_client.post(CATEGORY_URL, data)
        self.assertEqual(response.status_code, 201)
        # test title formal string -> 200
        self.assertEqual(response.data['data']['name'], data['name'].title())

        # admin client re-post same name -> 400
        response = self.admin_client.post(CATEGORY_URL, data)
        self.assertEqual(response.status_code, 400)


    def test_update_category(self):
        category_id = self.category_1.id
        url = CATEGORY_DETAIL_URL.format(category_id)
        data = {"name": "eyelash"}

        # anonymous and registered client put/post -> 403
        response = self.anonymous_client.put(url, data)
        self.assertEqual(response.status_code, 403)
        response = self.registered_client.post(url, data)
        self.assertEqual(response.status_code, 403)

        # admin client post data -> 405 wrong http method
        response = self.admin_client.post(url, data)
        self.assertEqual(response.status_code, 405)

        # admin client put empty -> 400
        response = self.admin_client.put(url, {})
        self.assertEqual(response.status_code, 400)

        # admin client put name -> 200
        response = self.admin_client.put(url, data)
        self.assertEqual(response.status_code, 200)
        # test title formal string
        self.assertEqual(response.data['data']['name'], data['name'].title())



    def test_delete_category(self):
        category_id = self.category_1.id
        url = CATEGORY_DETAIL_URL.format(category_id)

        # anonymous and registered client delete -> 403
        response = self.anonymous_client.delete(url)
        self.assertEqual(response.status_code, 403)
        response = self.registered_client.delete(url)
        self.assertEqual(response.status_code, 403)

        # admin client delete -> 200
        response = self.admin_client.delete(url)
        self.assertEqual(response.status_code, 200)

        response = self.admin_client.get(CATEGORY_URL)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['categories']), 2)

        self.assertEqual(response.data['categories'][0]['id'], self.category_2.id)
        self.assertEqual(response.data['categories'][1]['id'], self.category_3.id)
