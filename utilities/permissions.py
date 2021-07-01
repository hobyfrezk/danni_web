from rest_framework.permissions import BasePermission

class IsAdminUser(BasePermission):
    message = "You do not have permission to access this object."

    def has_permission(self, request, view):
        return request.user.is_superuser == True

    def has_object_permission(self, request, view, obj):
        return request.user.is_superuser == True


class IsNormalStaff(BasePermission):
    message = "You do not have permission to access this object."

    def has_permission(self, request, view):
        return True

    def has_object_permission(self, request, view, obj):
        return (request.user.is_staff == True) or (request.user.is_superuser == True)


class AllowAny(BasePermission):
    pass