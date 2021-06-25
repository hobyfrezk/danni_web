from rest_framework import serializers, exceptions

from categories.models import Category
from products.models import Product
from utilities.base_serializers import CategorySerializer


class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer()

    class Meta:
        model = Product
        fields = (
            'id',
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


class ProductSerializerForCreate(serializers.ModelSerializer):
    category_id = serializers.IntegerField()

    class Meta:
        model = Product
        fields = (
            'name',
            'price',
            'category_id',
            'created_at',
        )

    def validate(self, data):
        category_id = data['category_id']
        if not Category.objects.filter(id=category_id).exists():
            raise exceptions.ValidationError({'message': f'Category {category_id} does not exist.'})

        return data

    def create(self, validated_data):
        product = Product.objects.create(
            name=validated_data['name'].title(),
            price=validated_data['price'],
            category_id=validated_data['category_id'],
        )

        return product