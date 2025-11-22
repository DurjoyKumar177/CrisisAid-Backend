from rest_framework import permissions


class IsAuthenticatedOrCreateOnly(permissions.BasePermission):
    """
    Allow unauthenticated users to create (register),
    but require authentication for all other actions.
    """
    def has_permission(self, request, view):
        # Allow all POST requests (for social login and registration)
        if request.method == 'POST':
            return True
        # Check for ViewSet actions
        if hasattr(view, 'action') and view.action in ['create', 'register']:
            return True
        return request.user and request.user.is_authenticated


class IsOwner(permissions.BasePermission):
    """
    Custom permission to only allow users to access their own profile.
    """
    def has_object_permission(self, request, view, obj):
        return obj == request.user


class IsNGO(permissions.BasePermission):
    """
    Permission to check if user is an NGO (role-based)
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == "ngo"


class IsAdminUserOrReadOnly(permissions.BasePermission):
    """
    Read-only for regular users, full access for admin
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_authenticated and request.user.is_staff