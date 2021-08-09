from django.contrib.auth.models import User
from django.db import models

from utilities.cache_listeners import customer_changed, user_changed
from django.db.models.signals import post_save, pre_delete

from utilities.cache_listeners import user_changed, customer_changed

class Customer(models.Model):
    class Gender(models.IntegerChoices):
        NOT_GIVEN = (0, "Not Given")
        MALE = (1, "Male")
        FEMALE = (2, "Female")

    class Tier(models.IntegerChoices):
        NORMAL_USER = (0, "Normal User")
        TIER_1 = (1, "Tier 1")
        TIER_2 = (2, "Tier 2")
        TIER_3 = (3, "Tier 3")

    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, blank=True)
    first_name = models.CharField(max_length=16, null=True, blank=True)
    last_name = models.CharField(max_length=16, null=True, blank=True)
    gender = models.IntegerField(choices=Gender.choices, default=0)
    tier = models.IntegerField(choices=Tier.choices, default=0)

    phone = models.CharField(max_length=14, null=True, blank=True)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['created_at']
        indexes = [
            models.Index(fields=['user']),
            models.Index(fields=['balance']),
            models.Index(fields=['gender', 'created_at']),
            models.Index(fields=['tier'])
        ]

    def __str__(self):
        user_name = getattr(self.user, "username", "Null_user")
        return f"Username {user_name}"


def get_customer_data(user):
    from customers.services import CustomerService

    if hasattr(user, '_cached_customer_profile'):
        return getattr(user, '_cached_customer_profile')

    profile = CustomerService.get_customer_through_cache(user_id=user.id)
    setattr(user, '_cached_customer_profile', profile)

    return profile


User.customer = property(get_customer_data)

# hook up with listeners to invalidate cache
pre_delete.connect(user_changed, sender=User)
post_save.connect(user_changed, sender=User)

pre_delete.connect(customer_changed, sender=Customer)
post_save.connect(customer_changed, sender=Customer)