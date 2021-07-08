from rest_framework import serializers

from checkouts.models import Checkout

class CheckoutSerializer(serializers.ModelSerializer):
    class Meta:
        model = Checkout
        fields = ('id', 'user', 'appointment', 'served_by', 'products', "created_at")