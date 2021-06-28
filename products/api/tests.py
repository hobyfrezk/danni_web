from testing.testcases import TestCase

PRODUCT_URL = '/api/products/'
PRODUCT_URL_QUERY_CATEGORY = '/api/products/?category={}'
PRODUCT_URL_DETAIL = '/api/products/{}/'


class ProductsApiTest(TestCase):

    def setUp(self):
        """
        initialize_testing_accounts
            - self.anonymous_client,
            - self.registered_client,
            - self.admin_client,

        initialize_categories
            - self.category_1,
            - self.category_2,
            - self.category_3,
        """

        self.initialize_account()
        self.initialize_categories()

        self.product_1 = self.create_product(
            name="Spa Polish Manicure", price=25, category=self.category_1
        )
        self.product_2 = self.create_product(
            name="Spa Shellac Manicure", price=35, category=self.category_1
        )

    def test_list_products(self):
        # list with anonymous client -> 200
        # list with logged-in client -> 200
        # list with admin client -> 200
        # returned categories in created_at order -> 200
        for client in [self.anonymous_client, self.registered_client, self.admin_client]:
            response = client.get(PRODUCT_URL)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.data['success'], True)
            self.assertEqual(len(response.data['products']), 2)

            self.assertEqual(response.data['products'][0]['id'], self.product_1.id)
            self.assertEqual(response.data['products'][1]['id'], self.product_2.id)

    def test_list_products_under_specific_category(self):
        category_name = self.category_1.name
        url = PRODUCT_URL_QUERY_CATEGORY.format(category_name)

        # list with anonymous client -> 200
        # list with logged-in client -> 200
        # list with admin client -> 200
        # returned categories in created_at order -> 200

        for client in [self.anonymous_client, self.registered_client, self.admin_client]:
            response = client.get(url)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.data['success'], True)
            self.assertEqual(len(response.data['products']), 2)

            self.assertEqual(response.data['products'][0]['id'], self.product_1.id)
            self.assertEqual(response.data['products'][1]['id'], self.product_2.id)

    def test_create_products(self):
        # anonymous client post -> 403
        data = {
            "name": "product_name",
            "price": "25",
            "category_id": self.category_1.id
        }

        response = self.anonymous_client.post(PRODUCT_URL, data)
        self.assertEqual(response.status_code, 403)

        # logged-in client post -> 403
        response = self.registered_client.post(PRODUCT_URL, data)
        self.assertEqual(response.status_code, 403)

        # admin client post -> 201
        response = self.admin_client.post(PRODUCT_URL, data)
        self.assertEqual(response.status_code, 201)

        # admin client post same category same product -> 400
        response = self.admin_client.post(PRODUCT_URL, data)
        self.assertEqual(response.status_code, 400)


        # admin client post same category another product -> 201
        data = {
            "name": "product_name2",
            "price": "25",
            "category_id": self.category_1.id
        }
        response = self.admin_client.post(PRODUCT_URL, data)
        self.assertEqual(response.status_code, 201)

        # admin client post another category another product -> 201
        data = {
            "name": "product_name2",
            "price": "25",
            "category_id": self.category_2.id
        }
        response = self.admin_client.post(PRODUCT_URL, data)
        self.assertEqual(response.status_code, 201)

        # admin client post product without category -> 201
        data = {
            "name": "product_name2",
            "price": "25",
        }
        response = self.admin_client.post(PRODUCT_URL, data)
        self.assertEqual(response.status_code, 201)

    def test_update_products(self):
        data = {
            "name": "product_name",
            "price": "25",
            "category_id": self.category_1.id,
        }
        # admin client post -> 200
        response = self.admin_client.post(PRODUCT_URL, data)
        self.assertEqual(response.status_code, 201)
        product_id = response.data['id']

        update_url = PRODUCT_URL_DETAIL.format(product_id)

        updated_data = {
            "name": "product_name_updated",
            "price": "25",
            "category_id": self.category_2.id,
        }
        # non-admin client put -> 403
        response = self.anonymous_client.put(update_url, updated_data)
        self.assertEqual(response.status_code, 403)
        response = self.registered_client.put(update_url, updated_data)
        self.assertEqual(response.status_code, 403)

        # admin put -> 200
        response = self.admin_client.put(update_url, updated_data)
        self.assertEqual(response.status_code, 200)

    def test_delete_products(self):
        # delete with anonymous client -> 403
        # delete with logged-in client -> 403
        # delete with admin client -> 200
        url = PRODUCT_URL_DETAIL.format(self.product_1.id)
        for client in [self.anonymous_client, self.registered_client]:
            response = client.delete(url)
            self.assertEqual(response.status_code, 403)

        response = self.admin_client.delete(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['success'], True)

        response = self.admin_client.get(PRODUCT_URL)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['success'], True)
        self.assertEqual(len(response.data['products']), 1)

