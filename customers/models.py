from django.contrib.auth.models import User
from django.db import models


class Customer(models.Model):
    class Gender(models.IntegerChoices):
        NOT_GIVEN = (0, "Not Given")
        MALE = (1, "Male")
        FEMALE = (2, "Female")

    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True)
    first_name = models.CharField(max_length=16, null=True)
    last_name = models.CharField(max_length=16, null=True)
    gender = models.IntegerField(choices=Gender.choices, default=0)
    phone = models.CharField(max_length=14, null=True)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['created_at']
        indexes = [
            models.Index(fields=['user']),
            models.Index(fields=['balance']),
            models.Index(fields=['gender', 'created_at']),
        ]

    def __str__(self):
        user_name = getattr(self.user, "username", "Null_user")
        return f"Customer: {self.first_name} {self.last_name}. Username: {user_name}"

def _create_customer_profile(user):
    profile, _ = Customer.objects.get_or_create(user=user)
    return profile


def get_customer_data(user):
    if hasattr(user, '_cached_customer_profile'):
        return getattr(user, '_cached_customer_profile')

    profile = _create_customer_profile(user)
    setattr(user, '_cached_customer_profile', profile)

    return profile


User.customer = property(get_customer_data)
