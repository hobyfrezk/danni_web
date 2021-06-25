from rest_framework import serializers

from categories.models import Category

"""
base_serializers used to avoid Circular dependency in app/serializers.py
"""

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id','name', 'created_at')