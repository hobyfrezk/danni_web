from django.contrib.auth import (
    authenticate as django_authenticate,
    login as django_login,
    logout as django_logout,
)
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from accounts.api.serializers import SignupSerializer, LoginSerializer
from accounts.api.serializers import UserSerializer
from customers.api.serializers import CustomerSerializerForCreate


class AccountViewSet(viewsets.ViewSet):
    """
    API endpoints that allows: signup, login, login status, logout
    """

    serializer_class = SignupSerializer
    permissions_classes = (AllowAny,)

    @action(methods=['POST'], detail=False)
    def signup(self, request):
        """
        Signup with username, email, password (optional: first name, last name, gender, phone)
        """
        serializer_signup = SignupSerializer(data=request.data)
        serializer_customer = CustomerSerializerForCreate(data=request.data, context={'request': request})

        if not serializer_signup.is_valid():
            return Response({
                'success': False,
                'message': "Please check input",
                'errors': serializer_signup.errors,
            }, status=400)

        if not serializer_customer.is_valid():
            return Response({
                'success': False,
                'message': "Please check input",
                'errors': serializer_customer.errors,
            }, status=400)

        user = serializer_signup.save()
        serializer_customer.save()

        django_login(request, user)

        return Response({
            'success': True,
            'user': UserSerializer(user).data,
        }, status=201)

    @action(methods=['POST'], detail=False)
    def login(self, request):
        serializer = LoginSerializer(data=request.data)

        if not serializer.is_valid():
            return Response({
                "success": False,
                "message": "Please check input.",
                "errors": serializer.errors,
            }, status=400)

        username = serializer.validated_data['username'].lower()
        password = serializer.validated_data['password']
        user = django_authenticate(username=username, password=password)

        if not user or user.is_anonymous:
            return Response({
                "success": False,
                "message": "Username and password does not match.",
            }, status=400)

        django_login(request, user)
        user_data = {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "is_superuser": user.is_superuser,
        }

        return Response({
            "success": True,
            "user": user_data
        })

    @action(methods=['GET'], detail=False)
    def login_status(self, request):
        # check login status
        data = {'has_logged_in': request.user.is_authenticated}
        if request.user.is_authenticated:
            data['user'] = UserSerializer(request.user).data

        return Response(data)

    @action(methods=['POST'], detail=False)
    def logout(self, request):
        # logout
        django_logout(request)
        return Response({"success": True})
