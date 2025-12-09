# accounts/views.py
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView

from .forms import AdminUserCreateForm, AdminUserUpdateForm

User = get_user_model()


class SoloAdministradoresMixin(LoginRequiredMixin, UserPassesTestMixin):
    """
    Sólo permite acceso a administradores (o superusuarios/staff).
    """
    login_url = reverse_lazy("login")

    def test_func(self):
        user = self.request.user
        if not user.is_authenticated:
            return False

        rol = getattr(user, "rol", "")

        return (
            user.is_superuser
            or user.is_staff
            or rol in ["administrador", "admin"]
        )


class AdminUserListView(SoloAdministradoresMixin, ListView):
    """
    Lista de usuarios para el panel de administración.
    """
    model = User
    template_name = "accounts/admin_user_list.html"
    context_object_name = "usuarios"
    paginate_by = 20
    ordering = ["username"]


class AdminUserCreateView(SoloAdministradoresMixin, CreateView):
    """
    Crear nuevos usuarios desde el panel de admin.
    """
    model = User
    form_class = AdminUserCreateForm
    template_name = "accounts/admin_user_form.html"
    success_url = reverse_lazy("accounts:admin_user_list")


class AdminUserUpdateView(SoloAdministradoresMixin, UpdateView):
    """
    Editar usuarios existentes.
    """
