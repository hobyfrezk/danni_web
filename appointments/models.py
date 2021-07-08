from datetime import datetime, timedelta

import pytz
from django.contrib.auth.models import User
from django.db import models

from employees.models import Employee
from products.models import Product


class Appointment(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)

    appointment_time = models.DateTimeField()

    # duration of the appointment, count by minutes
    duration = models.IntegerField(default=0)

    services = models.ManyToManyField(Product)
    staff = models.ForeignKey(Employee, null=True, on_delete=models.SET_NULL)

    is_canceled = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = (
            models.Index(fields=['user']),
            models.Index(fields=['appointment_time']),
            models.Index(fields=['staff']),
        )

        ordering = ('created_at',)

    @property
    def is_expired(self):
        if datetime.now(pytz.utc) > self.end_time:
            return True
        return False

    @property
    def is_ongoing(self):
        now = datetime.now(pytz.utc)
        return self.appointment_time < now < self.end_time

    @property
    def end_time(self):
        time_change = timedelta(minutes=self.duration)
        return self.appointment_time + time_change
