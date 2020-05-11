from rest_framework.permissions import IsAuthenticated


class ShiftDetailPermission(IsAuthenticated):
    pass

    def has_object_permission(self, request, view, obj):
        return request.user == obj.user or request.user.roles.filter(label__in=['auditor', 'admin']).count() > 0