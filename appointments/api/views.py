from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from appointments.api.serializers import (
    AppointmentSerializer,
    AppointmentSerializerForCreate,
    AppointmentSerializerForCancel,
)
from appointments.models import Appointment
from utilities import permissions, helpers


class AppointmentViewSet(viewsets.GenericViewSet,
                         viewsets.mixins.ListModelMixin,
                         viewsets.mixins.RetrieveModelMixin,
                         viewsets.mixins.CreateModelMixin,
                         ):
    serializer_class = AppointmentSerializer
    queryset = Appointment.objects.all()

    def get_permissions(self):
        if self.action == "create":
            return [permissions.IsAuthenticated()]

        if self.action in ["retrieve", "cancel"]:
            return [permissions.IsObjectOwnerOrIsStaff()]

        return [permissions.IsStaff()]

    def list(self, request, *args, **kwargs):
        appointments = Appointment.objects.all()

        serializer = AppointmentSerializer(
            appointments,
            many=True,
        )

        return Response({
            'success': True,
            'appointments': serializer.data
        }, status=200)

    def retrieve(self, request, *args, **kwargs):
        appointment = self.get_object()

        return Response({
            'success': True,
            'appointment': AppointmentSerializer(appointment).data
        }, status=200)

    def create(self, request, *args, **kwargs):
        serializer = AppointmentSerializerForCreate(
            data=request.data, context={"request": request}
        )

        if not serializer.is_valid():
            return helpers.serializer_error_response(serializer)

        appointment = serializer.save()

        return Response({
            'success': True,
            'appointment': AppointmentSerializer(appointment).data
        }, status=201)

    @action(methods=["POST"], detail=True)
    def cancel(self, request, *args, **kwargs):
        appointment = self.get_object()

        serializer = AppointmentSerializerForCancel(
            instance=appointment
        )

        appointment = serializer.cancel()

        return Response({
            'success': True,
            'appointment': AppointmentSerializer(appointment).data
        }, status=201)

    @action(methods=["POST"], detail=False, url_path="staff-create")
    def staff_create(self, request):

        serializer = AppointmentSerializerForCancel(
            data=request.data
        )

        if not serializer.is_valid():
            return helpers.serializer_error_response(serializer)

        appointment = serializer.save()

        return Response({
            'success': True,
            'appointment': AppointmentSerializer(appointment).data
        }, status=201)
