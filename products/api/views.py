from django.shortcuts import get_object_or_404
from rest_framework import viewsets, permissions
from rest_framework.response import Response

from categories.models import Category
from products.api.serializers import ProductSerializerForCreate, ProductSerializer
from products.models import Product


class ProductViewSet(viewsets.GenericViewSet,
                     viewsets.mixins.ListModelMixin,
                     viewsets.mixins.CreateModelMixin,
                     viewsets.mixins.UpdateModelMixin,
                     viewsets.mixins.DestroyModelMixin,
                     ):
    """
    API endpoint that allows to :
        - List All Products
        - List Products under Specific Category
        - List Products under Specific Employee #TODO
        - Create Products
        - Update Products
        - Delete Product
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

    def list(self, request, *args, **kwargs):
        if 'category' in request.query_params:
            category_name = request.query_params.get('category').title()
            products = self._category_list_qs(category_name)
        else:
            products = Product.objects.all().prefetch_related('category')

        serializer = ProductSerializer(
            products, many=True,
        )

        return Response({
            'success': True,
            'products': serializer.data,
        })

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)

        return Response({
            "success": True
        }, status=200)