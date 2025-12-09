# accounts/admin.py

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    model = User

    # columnas en la lista de usuarios
    list_display = ("username", "email", "first_name", "last_name", "rol", "fecha_nacimiento", "is_staff")
    list_filter = ("rol", "is_staff", "is_superuser", "is_active", "groups")

    # campos al ver/editar un usuario
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        ("Información personal", {
            "fields": (
                "first_name",
                "last_name",
                "email",
                "rol",
                "fecha_nacimiento",
            )
        }),
        ("Permisos", {
            "fields": (
                "is_active",
                "is_staff",
                "is_superuser",
                "groups",
                "user_permissions",
            )
        }),
        ("Fechas importantes", {
            "fields": ("last_login", "date_joined")
        }),
    )

    # campos al crear un usuario desde el admin
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": (
                "username",
                "password1",
                "password2",
                "first_name",
                "last_name",
                "email",
                "rol",
                "fecha_nacimiento",
                "is_staff",
                "is_superuser",
                "is_active",
                "groups",
            ),
        }),
    )
