# eventos_vecinales/urls.py

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),

    # App principal de eventos
    path("", include(("events.urls", "events"), namespace="events")),

    # Login / logout / reset de contraseña de Django
    path("", include("django.contrib.auth.urls")),

    # Gestión de usuarios propia (crear/editar desde el panel)
    path("accounts/", include(("accounts.urls", "accounts"), namespace="accounts")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
