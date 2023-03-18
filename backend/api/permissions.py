from rest_framework import permissions


class IsStaffOrAuthorOrReadOnly(permissions.BasePermission):
    """Permissions for change or delete Admin or Author only"""
    message = 'Данное действие разрешено администратору или автору'

    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return bool(
            request.user.is_superuser
            or request.user.is_staff
            or obj.author == request.user
        )
