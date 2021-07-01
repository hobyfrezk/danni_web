from django.contrib.auth.models import User
from django.db import models

from products.models import Product


class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True)
    services = models.ManyToManyField(Product, blank=True)
    nickname = models.CharField(null=True, max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return 'staff: {}'.format(self.nickname)


def get_staff_data(user):
    if not user.is_staff:
        return None

    if hasattr(user, '_cached_staff_profile'):
        return getattr(user, '_cached_staff_profile')

    profile, _ = Employee.objects.get_or_create(user=user)
    setattr(user, '_cached_staff_profile', profile)

    return profile


User.staff = property(get_staff_data)
