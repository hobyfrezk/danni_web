from django.contrib import admin
from checkouts.models import Checkout

# Register your models here.
@admin.register(Checkout)
class CheckoutAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'appointment', 'served_by', "created_at")
    date_hierarchy = 'created_at'