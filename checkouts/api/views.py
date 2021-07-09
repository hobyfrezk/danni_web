from rest_framework import viewsets
from rest_framework.response import Response

from checkouts.api.serializers import CheckoutSerializer, CheckoutSerializerForCreate
from checkouts.models import Checkout
from utilities import permissions, helpers


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
        serializer = CheckoutSerializerForCreate(data=request.data, context={"request": request})

        if not serializer.is_valid():
            return helpers.serializer_error_response(serializer)

        checkout = serializer.save()

        return Response({
            'success': True,
            'checkouts': CheckoutSerializer(checkout).data
        }, status=201)