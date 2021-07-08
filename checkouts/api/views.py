from rest_framework import viewsets
from rest_framework.response import Response

from checkouts.api.serializers import CheckoutSerializer
from checkouts.models import Checkout
from utilities import permissions


class CheckoutViewSet(viewsets.GenericViewSet,
                      viewsets.mixins.ListModelMixin,
                      ):
    serializer_class = CheckoutSerializer
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
