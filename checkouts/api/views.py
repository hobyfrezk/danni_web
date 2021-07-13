from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from checkouts.api.serializers import CheckoutSerializer, CheckoutSerializerForCreate
from checkouts.models import Checkout
from customers.api.serializers import CustomerSerializerForUpdateBalance
from customers.models import Customer
from utilities import permissions, helpers
from django.db.models import F


class CheckoutViewSet(viewsets.GenericViewSet,
                      viewsets.mixins.ListModelMixin,
                      viewsets.mixins.CreateModelMixin,
                      ):
    serializer_class = CheckoutSerializerForCreate
    queryset = Checkout.objects.all()

    def get_permissions(self):
        return [permissions.IsStaff()]

    def list(self, request, *args, **kwargs):
        checkouts = Checkout.objects.all()

        serializer = CheckoutSerializer(checkouts, many=True)

        return Response({
            "success": True,
            "checkouts": serializer.data,
        }, status=200)

    def create(self, request, *args, **kwargs):
        checkout_serializer = CheckoutSerializerForCreate(data=request.data, context={"request": request})

        if not checkout_serializer.is_valid():
            return helpers.serializer_error_response(checkout_serializer)

        if request.data["type"] == "0":
            data = {"balance": helpers.calculate_spending_amount(
                request.data["amount"], request.data["pst"], request.data["gst"]
            )}
        elif request.data["type"] == "1":
            data = {"balance": request.data["amount"]}
        else:
            return helpers.checkouts_error_response()

        customer = Customer.objects.get(user_id=int(request.data["user"]))
        balance_serializer = CustomerSerializerForUpdateBalance(customer, data=data)

        if not balance_serializer.is_valid():
            return helpers.serializer_error_response(balance_serializer)

        checkout = checkout_serializer.save()
        balance_serializer.save()

        return Response({
            'success': True,
            'checkouts': CheckoutSerializer(checkout).data
        }, status=201)

    @action(methods=["POST"], detail=True)
    def delete(self, request, *args, **kwargs):
        checkout = self.get_object()
        checkout.is_deleted = True
        checkout.save()

        # atomic operation to update customer balance
        if checkout.type == 0:
            reverse_balance = -helpers.calculate_spending_amount(checkout.amount, checkout.pst, checkout.gst)
        else:
            reverse_balance = -checkout.amount
        Customer.objects.filter(user_id=checkout.user_id).update(balance=F('balance') + reverse_balance)

        return Response({
            'success': True,
            'checkout': CheckoutSerializer(checkout).data
        }, status=201)
