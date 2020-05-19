from rest_framework.permissions import IsAuthenticated, SAFE_METHODS


class ProductPermission(IsAuthenticated):
    def has_permission(self, request, view):
        if request.method == 'POST' or request.method == 'PATCH':
            return request.user.roles.filter(label__in=['auditor', 'admin']).count() > 0
        if request.method == 'DELETE':
            return False
        return True


class ProductExpiryPermission(IsAuthenticated):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        if request.method == 'DELETE':
            return False
        return request.user.roles.filter(label__in=['auditor', 'admin']).count() > 0
