from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from django.contrib.auth import get_user_model

from pegasio_serbia.users.forms import UserChangeForm, UserCreationForm

User = get_user_model()


@admin.register(User)
class UserAdmin(auth_admin.UserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    fieldsets = (("User", {"fields": ("name",'user_type')}),) + auth_admin.UserAdmin.fieldsets
    list_display = ["username", "name", 'user_type', 'email', "is_superuser"]
    search_fields = ["name"]
