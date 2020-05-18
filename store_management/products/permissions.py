from rest_framework.permissions import IsAuthenticated


class ProductPermission(IsAuthenticated):
    def has_permission(self, request, view):
        if request.method == 'POST' or request.method == 'PATCH':
            return request.user.roles.filter(label__in=['auditor', 'admin']).count() > 0
        return True

