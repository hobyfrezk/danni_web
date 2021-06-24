from django.contrib import admin
from categories.models import Category

# Register your models here.
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    # date_hierarchy = 'created_at'
    list_display = ('name', 'created_at')
