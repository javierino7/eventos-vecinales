# accounts/forms.py
from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()

# Estos valores deben calzar con tu modelo User.rol
ROL_CHOICES = [
    ("vecino", "Vecino / Usuario normal"),
    ("moderador", "Moderador"),
    ("administrador", "Administrador"),
]


class AdminUserCreateForm(forms.ModelForm):
    """
    Formulario para crear usuarios desde el panel de administrador.
    """

    password1 = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput(
            attrs={"class": "w3-input", "placeholder": "Contraseña"}
        ),
    )
    password2 = forms.CharField(
        label="Confirmar contraseña",
        widget=forms.PasswordInput(
            attrs={"class": "w3-input", "placeholder": "Repite la contraseña"}
        ),
    )

    rol = forms.ChoiceField(
        label="Rol",
        choices=ROL_CHOICES,
        widget=forms.Select(attrs={"class": "w3-select"}),
    )

    class Meta:
        model = User
        # Estos campos deben existir en tu modelo User
        fields = ["username", "email", "fecha_nacimiento", "is_active"]
        widgets = {
            "username": forms.TextInput(
                attrs={"class": "w3-input", "placeholder": "Nombre de usuario"}
            ),
            "email": forms.EmailInput(
                attrs={"class": "w3-input", "placeholder": "Correo electrónico"}
            ),
            "fecha_nacimiento": forms.DateInput(
                attrs={"type": "date", "class": "w3-input"}
            ),
        }
        labels = {
            "username": "Nombre de usuario",
            "email": "Correo electrónico",
            "fecha_nacimiento": "Fecha de nacimiento",
            "is_active": "Usuario activo",
        }

    def clean(self):
        cleaned_data = super().clean()
        p1 = cleaned_data.get("password1")
        p2 = cleaned_data.get("password2")
        if p1 and p2 and p1 != p2:
            self.add_error("password2", "Las contraseñas no coinciden.")
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)

        # Setear contraseña
        password = self.cleaned_data.get("password1")
        if password:
            user.set_password(password)

        # Asignar permisos según 'rol'
        rol = self.cleaned_data.get("rol")

        user.is_staff = False
        user.is_superuser = False

        if rol == "moderador":
            user.is_staff = True
        elif rol in ["administrador", "admin"]:
            user.is_staff = True
            user.is_superuser = True

        # Guardar también en el campo rol del modelo, si existe
        if hasattr(user, "rol"):
            user.rol = rol

        if commit:
            user.save()
        return user


class AdminUserUpdateForm(forms.ModelForm):
    """
    Formulario para editar usuarios existentes desde el panel admin.
    """

    rol = forms.ChoiceField(
        label="Rol",
        choices=ROL_CHOICES,
        widget=forms.Select(attrs={"class": "w3-select"}),
    )

    class Meta:
        model = User
        fields = ["username", "email", "fecha_nacimiento", "is_active"]
        widgets = {
            "username": forms.TextInput(
                attrs={"class": "w3-input", "placeholder": "Nombre de usuario"}
            ),
            "email": forms.EmailInput(
                attrs={"class": "w3-input", "placeholder": "Correo electrónico"}
            ),
            "fecha_nacimiento": forms.DateInput(
                attrs={"type": "date", "class": "w3-input"}
            ),
        }
        labels = {
            "username": "Nombre de usuario",
            "email": "Correo electrónico",
            "fecha_nacimiento": "Fecha de nacimiento",
            "is_active": "Usuario activo",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        user = self.instance
        if user:
            rol_actual = getattr(user, "rol", "")
            if rol_actual in ["vecino", "moderador", "administrador"]:
                self.initial["rol"] = rol_actual
            elif user.is_superuser:
                self.initial["rol"] = "administrador"
            elif user.is_staff:
                self.initial["rol"] = "moderador"
            else:
                self.initial["rol"] = "vecino"

    def save(self, commit=True):
        user = super().save(commit=False)

        rol = self.cleaned_data.get("rol")

        user.is_staff = False
        user.is_superuser = False

        if rol == "moderador":
            user.is_staff = True
        elif rol in ["administrador", "admin"]:
            user.is_staff = True
            user.is_superuser = True

        if hasattr(user, "rol"):
            user.rol = rol

        if commit:
            user.save()
        return user
