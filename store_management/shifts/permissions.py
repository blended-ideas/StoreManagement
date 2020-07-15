from rest_framework.permissions import IsAuthenticated


class ShiftDetailPermission(IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        return request.user == obj.user or request.user.roles.filter(label__in=['auditor', 'admin']).count() > 0


class ShiftEntryPermission(IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        return request.user == obj.shift.user or request.user.roles.filter(label__in=['auditor', 'admin']).count() > 0


class ShiftApprovePermission(IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        return request.user.roles.filter(label__in=['auditor', 'admin']).count() > 0


class ShiftAddProductApprovePermission(IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        return request.user.roles.filter(label__in=['auditor', 'admin']).count() > 0 or \
               (request.user == obj.user and obj.status == 'NEW')


class ShiftEntryPermission(IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        return request.user.roles.filter(label='admin').count() > 0 or \
               (request.user.roles.filter(label='auditor').count() > 0 and obj.shift.status != 'APPROVED')
