from django.conf import settings
from django.contrib.auth.models import User
from django.core.cache import caches

from backend.cache import USER_PATTERN

cache = caches['testing'] if settings.TESTING else caches['default']

class UserService:

    @classmethod
    def get_user_through_cache(cls, user_id):
        key = USER_PATTERN.format(user_id=user_id)

        # read from cache
        user = cache.get(key)

        if user is not None:
            settings.TESTING or print(f"GET USER FROM CACHE user_id={user_id}")
            return user

        try:
            user = User.objects.get(id=user_id)
            cache.set(key, user)
        except User.DoesNotExist:
            user = None
        return user


    @classmethod
    def invalidate_user(cls, user_id):
        key = USER_PATTERN.format(user_id=user_id)
        cache.delete(key)
