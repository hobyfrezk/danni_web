from django.contrib import admin
from customers.models import Customer
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = (
            'id',
            'user_id',
            'first_name',
            'last_name',
            'gender',
            'phone',
            'balance',
            'tier',
            'created_at',
            'updated_at'
        )

class CustomerInline(admin.StackedInline):
    model = Customer
    can_delete = False
    verbose_name_plural = 'Customer Profiles'

class UserAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'is_staff', 'date_joined')
    date_hierarchy = 'date_joined'
    inlines = (CustomerInline, )

admin.site.unregister(User)
admin.site.register(User, UserAdmin)