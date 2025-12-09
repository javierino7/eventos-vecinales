from django.contrib.auth import get_user_model
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from .forms import AdminUserCreateForm

User = get_user_model()


class SoloAdminMixin(UserPassesTestMixin):
    """
    Permite acceso solo a usuarios con rol = 'administrador'.
    """

    def test_func(self):
        user = self.request.user
        return user.is_authenticated and getattr(user, "rol", None) == "administrador"

    def handle_no_permission(self):
        messages.error(self.request, "No tienes permisos para acceder a esta sección.")
        from django.shortcuts import redirect
        return redirect("events:listar")


class AdminDashboardView(LoginRequiredMixin, SoloAdminMixin, TemplateView):
    template_name = "accounts/admin_dashboard.html"


class AdminUserCreateView(LoginRequiredMixin, SoloAdminMixin, CreateView):
    model = User
    form_class = AdminUserCreateForm
    template_name = "accounts/admin_user_create.html"
    success_url = reverse_lazy("accounts:admin_dashboard")

    def form_valid(self, form):
        messages.success(self.request, "Usuario creado correctamente.")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Revisa los errores del formulario.")
        return super().form_invalid(form)


class AdminEventModerationView(LoginRequiredMixin, SoloAdminMixin, TemplateView):
    """
    Vista placeholder para moderar eventos.
    La puedes completar luego con lógica real.
    """
    template_name = "accounts/admin_event_moderation.html"
