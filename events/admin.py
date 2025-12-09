# events/admin.py

from django.contrib import admin
from .models import Event, Inscripcion


class InscripcionInline(admin.TabularInline):
    model = Inscripcion
    extra = 0
    fields = ("usuario", "cantidad", "creado_en")
    readonly_fields = ("creado_en",)


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = (
        "titulo",
        "estado",
        "fecha_inicio",
        "fecha_termino",
        "cupos_totales",
        "cupos_ocupados",
        "creado_por",
        "creado_en",
    )
    list_filter = (
        "estado",
        "fecha_inicio",
        "solo_mayores_18",
        "creado_en",
    )
    search_fields = ("titulo", "descripcion", "localidad", "direccion", "lugar")
    readonly_fields = ("creado_en", "actualizado_en")
    inlines = [InscripcionInline]


@admin.register(Inscripcion)
class InscripcionAdmin(admin.ModelAdmin):
    list_display = ("event", "usuario", "cantidad", "creado_en")
    list_filter = ("event", "creado_en")
    search_fields = ("event__titulo", "usuario__email", "usuario__first_name", "usuario__last_name")
    readonly_fields = ("creado_en",)
