from rest_framework import permissions

class IsPostOwnerOrReadOnly(permissions.BasePermission):
    """
    Only the owner/managers of the crisis post can approve/reject volunteers.
    """
    def has_object_permission(self, request, view, obj):
        return obj.crisis_post.owner == request.user  # assuming CrisisPost has `owner` field

class IsVolunteerOwner(permissions.BasePermission):
    """
    Only the volunteer can view/update their own application.
    """
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user
