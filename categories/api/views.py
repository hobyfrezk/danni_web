from rest_framework import viewsets, permissions
from categories.models import Category
from categories.api.serializers import CategorySerializer


class CategoryViewSet(viewsets.GenericViewSet):
    queryset = Category.objects.all()
    serializer_class =