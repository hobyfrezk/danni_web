from django.conf import settings
from django.core.cache import caches

from backend.cache import CUSTOMER_PATTERN
from customers.models import Customer

cache = caches['testing'] if settings.TESTING else caches['default']

class CustomerService:

    @classmethod
    def get_customer_through_cache(cls, user_id):
        key = CUSTOMER_PATTERN.format(user_id=user_id)

        # read from cache
        customer = cache.get(key)

        if customer is not None:
            settings.TESTING or print(f"GET CUSTOMER FROM CACHE where user_id={user_id}")
            return customer

        try:
            customer, _ = Customer.objects.get_or_create(user_id=user_id)
            cache.set(key, customer)
        except Customer.DoesNotExist:
            customer = None
        return customer


    @classmethod
    def invalidate_customer(cls, user_id):
        key = CUSTOMER_PATTERN.format(user_id=user_id)
        cache.delete(key)
