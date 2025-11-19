from rest_framework import permissions

class IsUpdateCreatorOrReadOnly(permissions.BasePermission):
    """
    Only the creator of the update can edit/delete it.
    """
    def has_object_permission(self, request, view, obj):
        # Read permissions for everyone
        if request.method in permissions.SAFE_METHODS:
            return True
        # Write permissions only for creator
        return obj.created_by == request.user


class IsCommentOwnerOrReadOnly(permissions.BasePermission):
    """
    Only the comment owner can edit/delete their comment.
    """
    def has_object_permission(self, request, view, obj):
        # Read permissions for everyone
        if request.method in permissions.SAFE_METHODS:
            return True
        # Write permissions only for comment owner
        return obj.user == request.user


class CanCreateUpdate(permissions.BasePermission):
    """
    Only approved volunteers or post owner or admin can create updates.
    """
    def has_permission(self, request, view):
        if request.method != 'POST':
            return True
        
        # Must be authenticated
        if not request.user or not request.user.is_authenticated:
            return False
        
        # Admin can always create
        if request.user.is_staff:
            return True
        
        return True  # Let view handle specific crisis post permission