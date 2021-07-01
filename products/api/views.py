from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.response import Response

from categories.models import Category
from employees.models import Employee
from products.api.serializers import ProductSerializerForCreate, ProductSerializer
from products.models import Product
from utilities import permissions


class ProductViewSet(viewsets.GenericViewSet,
                     viewsets.mixins.ListModelMixin,
                     viewsets.mixins.CreateModelMixin,
                     viewsets.mixins.UpdateModelMixin,
                     viewsets.mixins.DestroyModelMixin,
                     viewsets.mixins.RetrieveModelMixin,
                     ):
    """
    API endpoint that allows to :
        - List All Products
        - List Products under Specific Category
        - List Products under Specific Employee
        - Retrieve a Product
        - Create Products
        - Update Products
        - Delete Product
        - Add product to Employee
    """

    queryset = Product.objects.all()
    serializer_class = ProductSerializerForCreate

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.AllowAny()]

        return [permissions.IsAdminUser()]

    @staticmethod
    def _category_list_qs(category_name):
        category_id = get_object_or_404(Category, name=category_name).id
        return Product.objects.filter(category=category_id).prefetch_related('category')

    @staticmethod
    def _employee_list_qs(employee_id):
        employee = get_object_or_404(Employee, id=employee_id)
        return employee.services.prefetch_related('category')

    def specific_query(self, query_params):
        if 'category' not in query_params and 'employee' not in query_params:
            return Response({
                'success': False,
                'message': "Please check input in requested URL.",
            }, status=400)

        if 'category' in query_params:
            category_name = query_params.get('category').title()
            products = self._category_list_qs(category_name)

        else:
            employee_id = query_params.get('employee')
            products = self._employee_list_qs(employee_id)

        serializer = ProductSerializer(
            products, many=True,
        )

        return Response({
            'success': True,
            'products': serializer.data,
        })

    @staticmethod
    def general_query():
        products = Product.objects.all().prefetch_related('category')

        serializer = ProductSerializer(
            products, many=True,
        )

        return Response({
            'success': True,
            'products': serializer.data,
        })


    def list(self, request, *args, **kwargs):
        if request.query_params:
            response = self.specific_query(request.query_params)
        else:
            response = self.general_query()
        return response

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)

        return Response({
            "success": True
        }, status=200)
