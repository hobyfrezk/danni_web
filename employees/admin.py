from django.contrib import admin
from employees.models import Employee


# Register your models here.
@admin.register(Employee)
class CategoryAdmin(admin.ModelAdmin):
    # date_hierarchy = 'created_at'
    list_display = ('id', 'user', 'nickname', 'created_at')
