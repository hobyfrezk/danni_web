from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from customers.api.serializers import (
    CustomerSerializer,
    CustomerSerializerForUpdateInfo,
    CustomerSerializerForUpdateBalance
)
from customers.models import Customer
from utilities import permissions


class CustomerViewSet(viewsets.GenericViewSet,
                      viewsets.mixins.ListModelMixin,
                      viewsets.mixins.RetrieveModelMixin,
                      ):
    """
    API endpoint that allows to:
        - List all customers
        - Retrieve a customer #TODO
        - Update info (first_name, last_name, gender, phone)
        - Update balance
        - List appointments #TODO
        - List checkouts #TODO
    """
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

    def get_permissions(self):
        if self.action in ['retrieve', 'update_info', 'list_appointments', 'list_checkouts']:
            return [permissions.IsAuthenticated(), permissions.IsObjectOwnerOrIsStaff()]

        if self.action in ['update_balance', 'list']:
            return [permissions.IsStaff()]

        return [permissions.IsAdminUser()]

    def list(self, request, *args, **kwargs):
        customers = Customer.objects.all()

        serializer = CustomerSerializer(
            customers, many=True,
        )

        return Response({
            'success': True,
            'customers': serializer.data,
        }, status=200)

    def retrieve(self, request, *args, **kwargs):
        customer = self.get_object()

        return Response({
            'success': True,
            'customer': CustomerSerializer(customer).data,
        }, status=200)

    @action(methods=["POST"], detail=True, url_path="update-info")
    def update_info(self, request, *args, **kwargs):
        customer = self.get_object()

        serializer = CustomerSerializerForUpdateInfo(
            instance=customer,
            data=request.data
        )

        if not serializer.is_valid():
            return Response({
                'message': 'Please check input',
                'error': serializer.errors,
            }, status=400)

        customer = serializer.save()

        return Response({
            'success': 'True',
            'customer': CustomerSerializer(customer).data
        }, status=200)

    @action(methods=["POST"], detail=True, url_path="update-balance")
    def update_balance(self, request, *args, **kwargs):
        # TODO fanout to checkout table
        customer = self.get_object()

        serializer = CustomerSerializerForUpdateBalance(
            instance=customer,
            data=request.data
        )

        if not serializer.is_valid():
            return Response({
                'message': 'Please check input',
                'error': serializer.errors,
            }, status=400)

        customer = serializer.save()

        return Response({
            'success': 'True',
            'customer': CustomerSerializer(customer).data
        }, status=200)
