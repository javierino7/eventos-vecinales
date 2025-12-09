# accounts/urls.py
from django.urls import path
from .views import (
    AdminUserListView,
    AdminUserCreateView,
    AdminUserUpdateView,
)

app_name = "accounts"

urlpatterns = [
    path("admin/usuarios/", AdminUserListView.as_view(), name="admin_user_list"),
    path("admin/usuarios/crear/", AdminUserCreateView.as_view(), name="admin_user_create"),
    path("admin/usuarios/<int:pk>/editar/", AdminUserUpdateView.as_view(), name="admin_user_edit"),
]
