from rest_framework import serializers, exceptions
from products.models import Product

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = (
            'name',
            'price',
            'category',
            'created_at',
        )

class ProductSerializerForCategory(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = (
            'name',
            'price',
            'created_at',
        )