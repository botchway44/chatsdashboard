from rest_framework import permissions

class IsAdminUser(permissions.BasePermission):
    """
    Allows access only to admin users.
    """
    def has_permission(self, request, view):
        # Check if the user is authenticated and has the 'ADMIN' role
        return request.user and request.user.is_authenticated and request.user.role == 'ADMIN'