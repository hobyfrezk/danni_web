from rest_framework import viewsets
from rest_framework.response import Response
from utilities import permissions

from categories.api.serializers import (
    CategorySerializer,
    CategorySerializerForCreate,
    CategorySerializerForUpdate,
    CategorySerializerForDetail,
)
from categories.models import Category


class CategoryViewSet(viewsets.GenericViewSet,
                      viewsets.mixins.ListModelMixin,
                      viewsets.mixins.CreateModelMixin,
                      viewsets.mixins.UpdateModelMixin,
                      viewsets.mixins.RetrieveModelMixin,
                      viewsets.mixins.DestroyModelMixin,
                      ):
    """
    API endpoint that allows to:
        - List All Categories
        - Retrieve a Category for details
        - Create Category
        - Update Category
        - Delete Category
    """

    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get_permissions(self):
        if self.action in ('list', 'retrieve'):
            return [permissions.AllowAny(),]

        return [permissions.IsAdminUser()]

    def list(self, request, *args, **kwargs):
        categories = Category.objects.all()
        serializer = CategorySerializer(
            categories, many=True,
        )

        return Response({
            'success': True,
            'categories': serializer.data,
        })

    def retrieve(self, request, *args, **kwargs):
        category = self.get_object()

        return Response({
            'success': True,
            'data': CategorySerializerForDetail(category).data
        })


    def create(self, request, *args, **kwargs):
        data = {
            'name': request.data.get('name'),
        }

        serializer = CategorySerializerForCreate(data=data)

        if not serializer.is_valid():
            return Response({
                'message': 'Please check input',
                'errors': serializer.errors,
            }, status=400)

        category = serializer.save()
        return Response({
            'success': True,
            'data': CategorySerializer(category).data,
        }, status=201)

    def update(self, request, *args, **kwargs):
        serializer = CategorySerializerForUpdate(
            instance=self.get_object(),
            data=request.data
        )

        if not serializer.is_valid():
            return Response({
                'message': 'Please check input',
                'error': serializer.errors,
            }, status=400)

        comment = serializer.save()
        return Response({
            'success': True,
            'data': CategorySerializer(comment).data,
        }, status=200)


    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)

        return Response({
            "success": True
        }, status=200)