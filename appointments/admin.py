from django.contrib import admin
from appointments.models import Appointment

# Register your models here.
@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'staff', 'appointment_time', 'duration', 'created_at')
    date_hierarchy = 'appointment_time'