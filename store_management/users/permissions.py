from rest_framework.permissions import IsAuthenticated, SAFE_METHODS


class UserPermissions(IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS and request.user.id == obj.id:
            return True
        return request.user.roles.filter(label='admin').count() > 0
