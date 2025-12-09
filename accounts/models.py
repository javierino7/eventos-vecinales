# accounts/models.py

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ROL_VECINO = "vecino"
    ROL_MODERADOR = "moderador"
    ROL_ADMIN = "administrador"

    ROL_CHOICES = [
        (ROL_VECINO, "Vecino"),
        (ROL_MODERADOR, "Moderador"),
        (ROL_ADMIN, "Administrador"),
    ]

    # Usa la columna 'role' que ya existe en la BD
    rol = models.CharField(
        max_length=20,
        choices=ROL_CHOICES,
        default=ROL_VECINO,
        db_column="role",
    )

    # Fecha de nacimiento para restricción +18
    fecha_nacimiento = models.DateField(
        null=True,
        blank=True,
        verbose_name="Fecha de nacimiento",
        help_text="Usada para validar eventos solo para mayores de 18 años.",
    )

    def save(self, *args, **kwargs):
        """
        Sincroniza el rol con los permisos de staff/superuser:

        - administradores y moderadores -> is_staff = True (pueden entrar a /admin)
        - vecinos -> is_staff = False
        - si el usuario es superuser, siempre se fuerza a rol 'administrador' y is_staff = True
        """
        if self.is_superuser:
            # Un superusuario siempre debe tener acceso completo al admin
            self.is_staff = True
            # De paso lo etiquetamos como administrador a nivel de rol
            if self.rol != self.ROL_ADMIN:
                self.rol = self.ROL_ADMIN
        else:
            # Para usuarios normales, el staff depende del rol
            if self.rol in (self.ROL_MODERADOR, self.ROL_ADMIN):
                self.is_staff = True
            else:
                self.is_staff = False

        super().save(*args, **kwargs)

    # ========= PERMISOS PERSONALIZADOS PARA EL ADMIN =========

    def has_module_perms(self, app_label):
        """
        Controla qué módulos (apps) puede ver en el admin.

        - superusuario: ve todo
        - moderador (staff): ve todo excepto accounts y auth
        - resto: comportamiento normal
        """
        if self.is_superuser:
            return True

        if self.is_staff and self.rol == self.ROL_MODERADOR:
            # Ocultar módulos de usuarios y grupos
            if app_label in ("accounts", "auth"):
                return False
            return True

        return super().has_module_perms(app_label)

    def has_perm(self, perm, obj=None):
        """
        Controla permisos específicos (add/change/delete/view).

        - superusuario: todo permitido
        - moderador (staff): todo menos cualquier permiso sobre usuarios/grupos
        - resto: comportamiento normal
        """
        if self.is_superuser:
            return True

        if self.is_staff and self.rol == self.ROL_MODERADOR:
            # perm viene como "app_label.codename"
            if perm.startswith("accounts.") or perm.startswith("auth."):
                return False
            return True

        return super().has_perm(perm, obj)

    def __str__(self):
        # Muestra username y rol
        return f"{self.username} ({self.rol})"
