from abc import ABC

from django.contrib.auth.models import User
from rest_framework import serializers, exceptions
from customers.api.serializers import CustomerSerializer

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'is_staff', 'is_superuser']


class UserSerializerWithProfileDetail(serializers.ModelSerializer):
    profile = serializers.SerializerMethodField()

    def get_profile(self, obj):
        return CustomerSerializer(obj.customer).data

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'is_staff', 'is_superuser', 'profile']


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        # check if user exists
        if not User.objects.filter(username=data['username'].lower()).exists():
            raise exceptions.ValidationError({
                'username': "User does not exist."
            })
        return data


class SignupSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=20, min_length=6)
    password = serializers.CharField(max_length=20, min_length=6)
    email = serializers.EmailField()


    class Meta:
        model = User
        fields = ('username', 'email', 'password')

    def is_valid_username(self, username):
        if len(username) < 8 or len(username) > 30:
            return False
        if '_' == username[0]:
            return False
        if ' ' in username:
            return False
        return True

    def validate(self, data):
        username = data['username'].lower()
        email = data['email'].lower()

        # check username validity
        if not self.is_valid_username(username):
            raise exceptions.ValidationError({
                'username': "Username is not valid."
            })

        # check username and email already exists.
        if User.objects.filter(username=username).exists():
            raise exceptions.ValidationError({
                'username': "This username has been occupied."
            })
        if User.objects.filter(email=email).exists():
            raise exceptions.ValidationError({
                'email': "This email has been occupied."
            })
        return data

    def create(self, validated_data):
        username = validated_data['username'].lower()
        email = validated_data['email'].lower()
        password = validated_data['password']

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
        )
        return user
