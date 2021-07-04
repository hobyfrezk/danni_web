from rest_framework.permissions import BasePermission, IsAuthenticated

PERMISSION_MSG = "You do not have permission to access this object."


class IsAdminUser(BasePermission):
    message = PERMISSION_MSG

    def has_permission(self, request, view):
        return request.user.is_superuser == True

    def has_object_permission(self, request, view, obj):
        return request.user.is_superuser == True


class IsStaff(BasePermission):
    message = PERMISSION_MSG

    def has_permission(self, request, view):
        return True

    def has_object_permission(self, request, view, obj):
        return (request.user.is_staff == True) or (request.user.is_superuser == True)


class AllowAny(BasePermission):
    pass


class IsObjectOwnerOrIsStaff(BasePermission):
    message = PERMISSION_MSG

    def has_permission(self, request, view):
        return True

    def has_object_permission(self, request, view, obj):
        return (request.user == obj.user) or \
               (request.user.is_staff == True) or \
               (request.user.is_superuser == True)