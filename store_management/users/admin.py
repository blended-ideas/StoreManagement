from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from django.contrib.auth import get_user_model

from store_management.users.forms import UserChangeForm, UserCreationForm
from .models import UserRole

admin.site.site_header = "Store Management"
admin.site.register(UserRole)

User = get_user_model()


@admin.register(User)
class UserAdmin(auth_admin.UserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    fieldsets = (("User", {"fields": ("name",)}),) + auth_admin.UserAdmin.fieldsets + (("Others", {"fields": ("roles",)}),)
    list_display = ["username", "name", "is_superuser"]
    search_fields = ["name"]
