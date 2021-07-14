from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from appointments.api.serializers import AppointmentSerializer
from appointments.models import Appointment
from checkouts.api.serializers import CheckoutSerializer
from checkouts.models import Checkout
from customers.api.serializers import (
    CustomerSerializer,
    CustomerSerializerForUpdateInfo,
    CustomerSerializerForUpdateTier
)
from customers.models import Customer
from utilities import permissions, helpers, paginations


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
        - Update tier
        - List appointments
        - List checkouts #TODO
    """
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    pagination_class = paginations.Pagination

    def get_permissions(self):
        if self.action in ['retrieve', 'update_info', 'list_appointments', 'list_checkouts', 'appointments',
                           "checkouts"]:
            return [permissions.IsAuthenticated(), permissions.IsObjectOwnerOrIsStaff()]

        if self.action in ['list', 'update_balance', 'update_tier']:
            return [permissions.IsStaff()]

        return [permissions.IsAdminUser()]

    def list(self, request, *args, **kwargs):
        customers = Customer.objects.all()
        page = self.paginate_queryset(customers)

        serializer = CustomerSerializer(page, many=True)

        return self.get_paginated_response(serializer.data)

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
            return helpers.serializer_error_response(serializer)

        customer = serializer.save()

        return Response({
            'success': 'True',
            'customer': CustomerSerializer(customer).data
        }, status=200)

    # @action(methods=["POST"], detail=True, url_path="update-balance")
    # def update_balance(self, request, *args, **kwargs):
    #     # TODO fanout to checkout table
    #     customer = self.get_object()
    #
    #     serializer = CustomerSerializerForUpdateBalance(
    #         instance=customer,
    #         data=request.data
    #     )
    #
    #     if not serializer.is_valid():
    #         return helpers.serializer_error_response(serializer)
    #
    #     customer = serializer.save()
    #
    #     return Response({
    #         'success': 'True',
    #         'customer': CustomerSerializer(customer).data
    #     }, status=200)

    @action(methods=["POST"], detail=True, url_path="update-tier")
    def update_tier(self, request, *args, **kwargs):
        customer = self.get_object()

        serializer = CustomerSerializerForUpdateTier(
            instance=customer,
            data=request.data
        )

        if not serializer.is_valid():
            return helpers.serializer_error_response(serializer)

        customer = serializer.save()

        return Response({
            'success': 'True',
            'customer': CustomerSerializer(customer).data
        }, status=200)

    @action(methods=["GET"], detail=True)
    def appointments(self, request, *args, **kwargs):
        customer = self.get_object()
        appointments = Appointment.objects.filter(user_id=customer.user_id)
        page = self.paginate_queryset(appointments)

        serializer = AppointmentSerializer(page, many=True)

        return self.get_paginated_response(serializer.data)

    @action(methods=["GET"], detail=True)
    def checkouts(self, request, *args, **kwargs):
        customer = self.get_object()
        checkouts = Checkout.objects.filter(user_id=customer.user_id)
        page = self.paginate_queryset(checkouts)

        serializer = CheckoutSerializer(page, many=True)

        return self.get_paginated_response(serializer.data)