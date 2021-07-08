"""backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from rest_framework import routers

from accounts.api.views import AccountViewSet
from categories.api.views import CategoryViewSet
from employees.api.views import EmployeeViewSet
from products.api.views import ProductViewSet
from customers.api.views import CustomerViewSet
from appointments.api.views import AppointmentViewSet


router = routers.DefaultRouter()
router.register(r'api/accounts', AccountViewSet, basename='accounts')
router.register(r'api/categories', CategoryViewSet, basename='categories')
router.register(r'api/products', ProductViewSet, basename='products')
router.register(r'api/employees', EmployeeViewSet, basename='employees')
router.register(r'api/customers', CustomerViewSet, basename='customers')
router.register(r'api/appointments', AppointmentViewSet, basename='appointments')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]
