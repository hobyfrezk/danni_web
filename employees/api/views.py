from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from appointments.api.serializers import AppointmentSerializer
from appointments.models import Appointment
from employees.api.serializers import (
    EmployeeSerializer,
    EmployeeSerializerForCreate,
    EmployeeSerializerForAddServices,
    EmployeeSerializerForRemoveServices,
)
from employees.models import Employee
from utilities import permissions, helpers


class EmployeeViewSet(viewsets.GenericViewSet,
                      viewsets.mixins.ListModelMixin,
                      viewsets.mixins.CreateModelMixin,
                      viewsets.mixins.DestroyModelMixin,
                      viewsets.mixins.RetrieveModelMixin,
                      ):
    """
    API endpoint that allows to:
        - List All Employees
        - Create New Employee
        - Retrieve An Employee
        - Delete An Employee
        - Update Service for An Employee
            - Add new service(s)
            - Delete service(s)
        - List Appointments for An Employee
    """

    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.AllowAny()]

        if self.action == "appointments":
            return [permissions.IsStaff()]

        return [permissions.IsAdminUser()]

    def list(self, request, *args, **kwargs):
        employees = Employee.objects.all().prefetch_related("user"). \
            prefetch_related('services__category')

        serializer = EmployeeSerializer(
            employees, many=True,
        )

        return Response({
            'success': True,
            'employees': serializer.data,
        }, status=200)

    def create(self, request, *args, **kwargs):
        serializer = EmployeeSerializerForCreate(
            data=request.data
        )

        if not serializer.is_valid():
            return helpers.serializer_error_response(serializer)

        employee = serializer.save()

        user = employee.user
        user.is_staff = True
        user.save()

        return Response({
            "success": True,
            "employee": EmployeeSerializer(employee).data
        }, status=201)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)

        user = instance.user
        user.is_staff = False
        user.save()

        return Response({
            "success": True,
        }, status=200)

    @action(methods=['POST'], detail=True, url_path='add-services')
    def add_services(self, request, *args, **kwargs):
        employee = self.get_object()

        serializer = EmployeeSerializerForAddServices(
            employee, data=request.data
        )

        if not serializer.is_valid():
            return helpers.serializer_error_response(serializer)

        employee = serializer.save()

        return Response({
            'success': True,
            'employee': EmployeeSerializer(employee).data,
        }, status=201)

    @action(methods=['POST'], detail=True, url_path='remove-services')
    def remove_services(self, request, *args, **kwargs):
        employee = self.get_object()

        serializer = EmployeeSerializerForRemoveServices(
            employee, data=request.data
        )

        if not serializer.is_valid():
            return helpers.serializer_error_response(serializer)

        employee = serializer.save()

        return Response({
            'success': True,
            'employee': EmployeeSerializer(employee).data,
        }, status=201)

    @action(methods=["GET"], detail=True)
    def appointments(self, request, *args, **kwargs):
        employee = self.get_object()
        appointments = Appointment.objects.filter(staff=employee)

        serializer = AppointmentSerializer(appointments, many=True)

        return Response({
            'success': 'True',
            'appointments': serializer.data
        }, status=200)
