from django.contrib.auth.models import User
from rest_framework import serializers, exceptions

from customers.models import Customer


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = (
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


class CustomerSerializerForCreate(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = (
            'user',
            'first_name',
            'last_name',
            'gender',
            'phone',
        )

    def validate(self, data):
        # TODO validate phone
        return data

    def create(self, validated_data):
        user = User.objects.filter(username=self.context['request'].data['username'].lower()).first()
        first_name = validated_data.get('first_name', '').lower()
        last_name = validated_data.get('last_name', '').lower()
        gender = validated_data.get('gender', 0)
        phone = validated_data.get('phone', '')

        user = Customer.objects.create(
            user=user, first_name=first_name, last_name=last_name, gender=gender, phone=phone,
        )

        return user


class CustomerSerializerForUpdateInfo(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = (
            'user',
            'first_name',
            'last_name',
            'gender',
            'phone',
        )

    def update(self, instance, validated_data):
        for key in validated_data:
            setattr(instance, key, validated_data[key])

        instance.save()
        return instance


class CustomerSerializerForUpdateBalance(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ('balance',)

    def validate(self, data):
        if self.instance.balance + data["balance"] <= 0:
            raise exceptions.ValidationError({
                'Balance': "Error: Over spending, balance will be negative after this checkout."
            })

        return data

    def update(self, instance, validated_data):
        instance.balance += validated_data['balance']

        instance.save()
        return instance


class CustomerSerializerForUpdateTier(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ('tier',)

    def update(self, instance, validated_data):
        instance.tier = validated_data['tier']

        instance.save()
        return instance
