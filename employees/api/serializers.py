from rest_framework import serializers

from accounts.api.serializers import UserSerializer
from employees.models import Employee
from products.api.serializers import ProductSerializer


class EmployeeSerializer(serializers.ModelSerializer):
    services = ProductSerializer(many=True)
    user = UserSerializer()

    class Meta:
        model = Employee
        fields = ('id', 'user', 'services', 'nickname', 'created_at')


class EmployeeSerializerForCreate(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ('user', 'services', 'nickname')

    def create(self, validated_data):
        user = validated_data['user']
        services = validated_data['services']
        nickname = validated_data['nickname']

        user.is_staff = True
        user.save()

        employee = Employee.objects.create(user=user, nickname=nickname)
        employee.services.add(*services)

        return employee


class BaseEmployeeSerializerForUpdateService(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ('services',)


class EmployeeSerializerForAddServices(BaseEmployeeSerializerForUpdateService):

    def update(self, instance, validated_data):
        instance.services.add(*validated_data['services'])
        instance.save()

        return instance


class EmployeeSerializerForRemoveServices(BaseEmployeeSerializerForUpdateService):

    def update(self, instance, validated_data):
        instance.services.remove(*validated_data['services'])
        instance.save()

        return instance
