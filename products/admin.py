from django.contrib import admin
from products.models import Product


# Register your models here.

@admin.register(Product)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('category', 'name', 'price', 'created_at')