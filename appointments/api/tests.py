# list appointment
# retrieve appointment
# create appointment
# cancel appointment
# test is_expired
# test is_ongoing
# get appointment under a customer
# get appointment under a employee


from datetime import datetime, timedelta

import pytz

from appointments.models import Appointment
from testing.testcases import TestCase

APPOINTMENTS_URL = '/api/appointments/'
APPOINTMENTS_DETAIL_URL = '/api/appointments/{}/'
CANCEL_URL = '/api/appointments/{}/cancel/'
STAFF_CREATE_URL = '/api/appointments/staff-create/'

class AppointmentsTest(TestCase):

    def setUp(self):
        """
        initialize_testing_accounts()
            - self.anonymous_client,
            - self.registered_client,
            - self.registered_client2,
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
        self.clear_cache()

        self.initialize_account()
        self.initialize_categories()
        self.initialize_products()
        self.initialize_appointments()


    def test_models(self):
        self.assertEqual(Appointment.objects.count(), 3)

        self.assertEqual(self.appointment_1.is_ongoing, False)
        self.assertEqual(self.appointment_1.is_expired, False)

        self.assertEqual(self.appointment_2.is_ongoing, False)
        self.assertEqual(self.appointment_2.is_expired, True)

        self.assertEqual(self.appointment_3.is_ongoing, True)
        self.assertEqual(self.appointment_3.is_expired, False)

    def test_list(self):
        response = self.anonymous_client.get(APPOINTMENTS_URL)
        self.assertEqual(response.status_code, 403)

        response = self.registered_client.get(APPOINTMENTS_URL)
        self.assertEqual(response.status_code, 403)

        response = self.staff_client.get(APPOINTMENTS_URL)
        self.assertEqual(response.status_code, 200)
        appointments = response.data.get("data")
        self.assertEqual(len(appointments), 3)
        self.assertEqual(appointments[0]["id"], self.appointment_1.id)
        self.assertEqual(appointments[1]["id"], self.appointment_2.id)
        self.assertEqual(appointments[2]["id"], self.appointment_3.id)

        response = self.admin_client.get(APPOINTMENTS_URL)
        self.assertEqual(response.status_code, 200)
        appointments = response.data.get("data")
        self.assertEqual(len(appointments), 3)
        self.assertEqual(appointments[0]["id"], self.appointment_1.id)
        self.assertEqual(appointments[1]["id"], self.appointment_2.id)
        self.assertEqual(appointments[2]["id"], self.appointment_3.id)

    def test_retrieve(self):
        retrieve_url = APPOINTMENTS_DETAIL_URL.format(self.appointment_1.id)

        response = self.anonymous_client.get(retrieve_url)
        self.assertEqual(response.status_code, 403)

        response = self.registered_client.get(retrieve_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["appointment"]["user"]["id"], self.registered_user.id)

        response = self.staff_client.get(retrieve_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["appointment"]["user"]["id"], self.registered_user.id)

        response = self.admin_client.get(retrieve_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["appointment"]["user"]["id"], self.registered_user.id)

    def test_client_create(self):
        data = {
            "appointment_time": (datetime.now(pytz.utc) + timedelta(hours=48)).strftime("%Y-%m-%d %H:%M:%S"),
            "duration": "60",
            "services": [self.product_1.id, self.product_2.id],
            "staff": self.staff_user.staff.id,
        }

        response = self.anonymous_client.post(APPOINTMENTS_URL, data)
        self.assertEqual(response.status_code, 403)

        response = self.registered_client.post(APPOINTMENTS_URL, data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["appointment"]["user"]["id"], self.registered_user.id)
        self.assertEqual(response.data["appointment"]["services"], [self.product_1.id, self.product_2.id])
        self.assertEqual(response.data["appointment"]["staff"], self.staff_user.staff.id)

        # overbook
        response = self.registered_client.post(APPOINTMENTS_URL, data)
        self.assertEqual(response.status_code, 400)

    def test_cancel(self):
        cancel_url = CANCEL_URL.format(self.appointment_1.id)

        response = self.anonymous_client.post(cancel_url)
        self.assertEqual(response.status_code, 403)

        response = self.registered_client.post(cancel_url)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["appointment"]["id"], self.appointment_1.id)

        response = self.registered_client2.post(cancel_url)
        self.assertEqual(response.status_code, 403)

        response = self.staff_client.post(cancel_url)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["appointment"]["id"], self.appointment_1.id)

        response = self.admin_client.post(cancel_url)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["appointment"]["id"], self.appointment_1.id)

        wrong_cancel_url = CANCEL_URL.format(9527)
        response = self.staff_client.post(wrong_cancel_url)
        self.assertEqual(response.status_code, 404)

    def test_staff_create(self):
        data = {
            "user": self.registered_user.id,
            "appointment_time": (datetime.now(pytz.utc) + timedelta(hours=48)).strftime("%Y-%m-%d %H:%M:%S"),
            "duration": "60",
            "services": [self.product_1.id, self.product_2.id],
            "staff": self.admin_user.staff.id,
        }

        response = self.anonymous_client.post(STAFF_CREATE_URL, data)
        self.assertEqual(response.status_code, 403)

        response = self.registered_client.post(STAFF_CREATE_URL, data)
        self.assertEqual(response.status_code, 403)

        response = self.staff_client.post(STAFF_CREATE_URL, data)
        self.assertEqual(response.status_code, 201)

        # overbook -> 400
        response = self.staff_client.post(STAFF_CREATE_URL, data)
        self.assertEqual(response.status_code, 400)


