from rest_framework import serializers, exceptions
from categories.models import Category

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id','name', 'created_at')

class CategorySerializerForCreate(serializers.ModelSerializer):
    name = serializers.CharField()

    class Meta:
        model = Category
        fields = ('name', )

    def validate(self, data):
        # check if already exist
        name = data['name'].title()

        if not name:
            raise exceptions.ValidationError({'message': f'category name cannot be empty.'})

        if Category.objects.filter(name=name).exists():
            raise exceptions.ValidationError({'message': f'category: {name} already exists.'})
        return data

    def create(self, validated_data):
        category = Category.objects.create(name=validated_data['name'].title())
        return category


class CategorySerializerForUpdate(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name', )

    def validate(self, data):
        # check if already exist
        name = data['name'].title()

        if not name:
            raise exceptions.ValidationError({'message': f'category name cannot be empty.'})

        return data

    def update(self, instance, validated_data):
        instance.name = validated_data['name'].title()
        instance.save()

        return instance