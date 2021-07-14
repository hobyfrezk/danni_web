from rest_framework import serializers

from appointments.models import Appointment


class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = (
            'id', 'user', 'appointment_time', 'duration', 'services', 'staff', 'is_canceled', 'created_at', 'updated_at'
        )


class AppointmentSerializerForCreate(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = ('user', 'appointment_time', 'duration', 'services', 'staff')

    def validate(self, data):
        # TODO validate：
        #  - duration must longer than selected products
        #  - staff is free during selected duration,
        #  - but those considerations can be released when staff want to create appointments.
        #    in `AppointmentSerializerForStaffCreate`

        return data

    def create(self, validated_data):
        user = validated_data["user"]
        appointment_time = validated_data["appointment_time"]
        duration = validated_data["duration"]
        services = validated_data["services"]
        staff = validated_data["staff"]

        appointment = Appointment.objects.create(
            user=user, appointment_time=appointment_time, duration=duration, staff=staff
        )

        appointment.services.add(*services)
        appointment.save()

        return appointment


class AppointmentSerializerForCancel(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = ('is_canceled',)

    def cancel(self):
        self.instance.is_canceled = True
        self.instance.save()

        return self.instance


class AppointmentSerializerForStaffCreate(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = ('user', 'appointment_time', 'duration', 'services', 'staff')

    def create(self, validated_data):
        user = validated_data["user"]
        appointment_time = validated_data["appointment_time"]
        duration = validated_data["duration"]
        services = validated_data["services"]
        staff = validated_data["staff"]

        appointment = Appointment.objects.create(
            user=user, appointment_time=appointment_time, duration=duration, staff=staff
        )

        appointment.services.add(*services)
        appointment.save()

        return appointment
