# events/urls.py
from django.urls import path

from .views import (
    EventListView,
    EventDetailView,
    EventCreateView,
    EventUpdateView,
    EventDeleteView,
    MisEventosListView,
    AdminPanelView,
    cambiar_estado_evento,
    asistir,
    checkout_exito,
)

app_name = "events"

urlpatterns = [
    path("", EventListView.as_view(), name="listar"),
    path("eventos/", EventListView.as_view(), name="lista"),

    path("eventos/crear/", EventCreateView.as_view(), name="crear"),
    path("eventos/<int:pk>/", EventDetailView.as_view(), name="detalle"),
    path("eventos/<int:pk>/editar/", EventUpdateView.as_view(), name="editar"),
    path("eventos/<int:pk>/eliminar/", EventDeleteView.as_view(), name="eliminar"),

    path("mis-eventos/", MisEventosListView.as_view(), name="mis_eventos"),

    path("panel-admin/", AdminPanelView.as_view(), name="panel_admin"),
    path(
        "panel-admin/eventos/<int:pk>/<str:nuevo_estado>/",
        cambiar_estado_evento,
        name="cambiar_estado_evento",
    ),

    path("<int:pk>/asistir/", asistir, name="asistir"),
    path("<int:pk>/asistir/exito/", checkout_exito, name="checkout_exito"),
]
