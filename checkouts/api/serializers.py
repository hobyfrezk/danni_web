from rest_framework import serializers, exceptions

from checkouts.models import Checkout


class CheckoutSerializer(serializers.ModelSerializer):
    class Meta:
        model = Checkout
        fields = ('id', 'user', 'appointment', 'served_by', 'products', "notes", "checkout_snapshot", "created_at")


class CheckoutSerializerForCreate(serializers.ModelSerializer):
    class Meta:
        model = Checkout
        fields = (
            "user",
            "appointment",
            "served_by",
            "checked_by",
            "products",
            "type",
            "amount",
            "pst",
            "gst",
            "checkout_snapshot",
            "notes"
        )

    def validate(self, data):
        user = data["user"]
        appointment = data["appointment"]

        if user != appointment.user:
            raise exceptions.ValidationError({
                'Appointment': "Referred appointment is not coincidence with user."
            })

        return data

    def create(self, validated_data):
        data = {
            **validated_data,
            "checked_by": self.context["request"].user.staff
        }

        products = data["products"]
        del data["products"]

        checkout = Checkout.objects.create(
            **data
        )

        checkout.products.add(*products)
        checkout.save()

        return checkout

