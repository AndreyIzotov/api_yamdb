from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group

from users.forms import UserChangeForm, UserCreationForm
from users.models import User


class UserAdmin(BaseUserAdmin):
    """Профиль админа"""

    form = UserChangeForm
    add_form = UserCreationForm
    list_display = ('id', 'email', 'username', 'is_active', 'role',
                    'bio', 'first_name', 'last_name', 'confirmation_code')
    list_filter = ('is_admin',)
    fieldsets = (
        (None, {'fields': ('email', 'password', 'role')}),
        ('Permissions', {'fields': ('is_admin', 'is_staff', 'is_superuser')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'role', 'password1', 'password2'),
        }),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()


admin.site.register(User, UserAdmin)


admin.site.unregister(Group)
