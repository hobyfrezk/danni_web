from django.contrib.auth.models import User
from django.db import models

from appointments.models import Appointment
from employees.models import Employee
from products.models import Product


class Checkout(models.Model):
    class Type(models.IntegerChoices):
        SPENDING = (0, "Spending")
        RECHARGE = (1, "Recharge")
        MIXING = (2, "Recharge and Spending")

    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    appointment = models.ForeignKey(Appointment, null=True, on_delete=models.SET_NULL)

    served_by = models.ForeignKey(Employee,
                                  null=True,
                                  on_delete=models.SET_NULL,
                                  related_name="served_checkout_set")

    checked_by = models.ForeignKey(Employee,
                                   null=True,
                                   on_delete=models.SET_NULL,
                                   related_name="checked_checkout_set")

    products = models.ManyToManyField(Product, blank=True)
    type = models.IntegerField(choices=Type.choices)
    amount = models.DecimalField(decimal_places=2, max_digits=12)

    pst = models.DecimalField(decimal_places=2, max_digits=2)
    gst = models.DecimalField(decimal_places=2, max_digits=2)

    checkout_snapshot = models.TextField()
    notes = models.TextField(null=True)

    is_deleted = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = (
            models.Index(fields=['user']),
            models.Index(fields=['served_by']),
            models.Index(fields=['checked_by']),
            models.Index(fields=["created_at"])
        )

        ordering = ("created_at",)
