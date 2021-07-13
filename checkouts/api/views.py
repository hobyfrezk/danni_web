from rest_framework import viewsets
from rest_framework.response import Response

from checkouts.api.serializers import CheckoutSerializer, CheckoutSerializerForCreate
from checkouts.models import Checkout
from utilities import permissions, helpers
from customers.api.serializers import CustomerSerializerForUpdateBalance
from customers.models import Customer

class CheckoutViewSet(viewsets.GenericViewSet,
                      viewsets.mixins.ListModelMixin,
                      viewsets.mixins.CreateModelMixin,
                      viewsets.mixins.DestroyModelMixin,
                      viewsets.mixins.UpdateModelMixin,
                      viewsets.mixins.RetrieveModelMixin,
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