# events/models.py

from django.conf import settings
from django.db import models
from django.db.models import Sum
from django.utils import timezone


def event_image_upload_to(instance, filename):
    """
    Carpeta donde se guardan las imágenes de eventos.
    """
    return f"eventos/{instance.id or 'nuevo'}/{filename}"


class Event(models.Model):
    # Estados posibles del evento
    ESTADO_PENDIENTE = "pendiente"
    ESTADO_APROBADO = "aprobado"
    ESTADO_RECHAZADO = "rechazado"

    ESTADO_CHOICES = (
        (ESTADO_PENDIENTE, "Pendiente de aprobación"),
        (ESTADO_APROBADO, "Aprobado"),
        (ESTADO_RECHAZADO, "Rechazado"),
    )

    # --- Campos principales (coinciden con tu BD) ---

    titulo = models.CharField(max_length=200)
    descripcion = models.TextField()

    estado = models.CharField(
        max_length=20,
        choices=ESTADO_CHOICES,
        default=ESTADO_PENDIENTE,
    )

    creado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="eventos_creados",
    )

    creado_en = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    actualizado_en = models.DateTimeField(auto_now=True, null=True, blank=True)

    imagen = models.ImageField(
        upload_to=event_image_upload_to,
        null=True,
        blank=True,
    )

    # Dirección y ubicación
    direccion = models.CharField(max_length=255, default="")
    localidad = models.CharField(max_length=100, null=True, blank=True)
    lugar = models.CharField(max_length=150, null=True, blank=True)

    # Campo hora original que ya existe en la BD
    hora = models.TimeField(null=True, blank=True)

    # Campo de texto antiguo de ubicación (lo dejamos por compatibilidad)
    ubicacion = models.CharField(max_length=255, null=True, blank=True)

    # Fechas y horarios nuevos
    fecha_inicio = models.DateField(null=True, blank=True)
    fecha_termino = models.DateField(null=True, blank=True)
    hora_inicio = models.TimeField(null=True, blank=True)
    hora_termino = models.TimeField(null=True, blank=True)

    # Cupos totales del evento (0 = sin límite)
    cupos_totales = models.PositiveIntegerField(default=0)

    # Restricción de edad
    solo_mayores_18 = models.BooleanField(
        default=False,
        help_text="Si está marcado, solo pueden asistir personas mayores de 18 años.",
    )

    # Precio por entrada (0 = gratuito)
    precio_entrada = models.DecimalField(
        max_digits=8,
        decimal_places=0,
        default=0,
        help_text="Precio de la entrada por persona en pesos chilenos.",
    )

    # Asistentes (relación simple para estadísticas y filtros)
    asistentes = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="eventos_asistidos",
        blank=True,
    )

    class Meta:
        verbose_name = "Evento"
        verbose_name_plural = "Eventos"
        ordering = ("fecha_inicio", "hora_inicio", "titulo")

    def __str__(self) -> str:
        return self.titulo

    # --------- Cupos usando Inscripcion ----------

    @property
    def cupos_ocupados(self) -> int:
        """
        Suma de todas las entradas reservadas (cantidad) para este evento.
        """
        total = self.inscripciones.aggregate(total=Sum("cantidad"))["total"]
        return total or 0

    @property
    def cupos_disponibles(self):
        """
        Cupos restantes considerando la suma de cantidades de inscripciones.
        Si cupos_totales es 0 se considera 'sin límite' y retorna None.
        """
        if not self.cupos_totales:
            return None  # sin límite
        restantes = self.cupos_totales - self.cupos_ocupados
        return max(restantes, 0)

    @property
    def esta_lleno(self) -> bool:
        """
        True si el evento tiene límite de cupos y ya no queda ninguno.
        """
        if not self.cupos_totales:
            # 0 = sin límite => nunca se considera lleno
            return False
        return self.cupos_disponibles <= 0

    @property
    def es_gratuito(self) -> bool:
        """
        True si el precio de la entrada es 0 o menor.
        """
        return not self.precio_entrada or self.precio_entrada <= 0

    # --------- Ayudas de tiempo / colores ----------

    @property
    def es_proximo(self):
        """
        True si el evento aún no termina (comparación por fecha).
        """
        if not self.fecha_termino and not self.fecha_inicio:
            return False
        hoy = timezone.localdate()
        fecha_fin = self.fecha_termino or self.fecha_inicio
        return fecha_fin >= hoy

    @property
    def css_clase_tiempo(self):
        """
        Devuelve una clase CSS según cuánto falta para el inicio del evento.
        """
        if not self.fecha_inicio:
            return "badge-tiempo--sin-fecha"

        hoy = timezone.localdate()
        delta = (self.fecha_inicio - hoy).days

        if delta < 0:
            return "badge-tiempo--pasado"       # ya ocurrió
        elif delta == 0:
            return "badge-tiempo--hoy"          # es hoy
        elif 1 <= delta <= 3:
            return "badge-tiempo--muy-pronto"   # en los próximos 3 días
        elif 4 <= delta <= 7:
            return "badge-tiempo--esta-semana"  # dentro de la semana
        else:
            return "badge-tiempo--mas-adelante" # más adelante

    @property
    def texto_tiempo(self):
        """
        Texto amigable que acompaña el color del tiempo.
        """
        if not self.fecha_inicio:
            return "Fecha por definir"

        hoy = timezone.localdate()
        delta = (self.fecha_inicio - hoy).days

        if delta < 0:
            return "Evento pasado"
        elif delta == 0:
            return "Es hoy"
        elif delta == 1:
            return "Mañana"
        elif 2 <= delta <= 3:
            return f"En {delta} días"
        elif 4 <= delta <= 7:
            return "Esta semana"
        else:
            return "Próximamente"

    @property
    def esta_finalizado(self) -> bool:
        """
        True si la fecha de término del evento ya pasó.
        """
        if not self.fecha_termino and not self.fecha_inicio:
            return False
        hoy = timezone.localdate()
        fecha_fin = self.fecha_termino or self.fecha_inicio
        return fecha_fin < hoy

    @property
    def estado_tiempo(self) -> str:
        """
        Estado textual según el tiempo:
        - 'finalizado'
        - 'hoy'
        - 'pronto' (menos de 3 días)
        - 'normal'
        """
        if self.esta_finalizado:
            return "finalizado"

        if not self.fecha_inicio:
            return "normal"

        hoy = timezone.localdate()
        delta = (self.fecha_inicio - hoy).days

        if delta == 0:
            return "hoy"
        if 1 <= delta <= 3:
            return "pronto"
        return "normal"

    @property
    def estado_tiempo_clase(self) -> str:
        """
        Clases CSS para colorear la card según el tiempo.
        """
        mapping = {
            "finalizado": "border-danger bg-danger-subtle",
            "hoy": "border-success bg-success-subtle",
            "pronto": "border-warning bg-warning-subtle",
            "normal": "border-light bg-body",
        }
        return mapping.get(self.estado_tiempo, "border-light bg-body")


class Inscripcion(models.Model):
    """
    Inscripción de un usuario a un evento con cantidad de entradas.
    Máximo 5 entradas por usuario (se controla en la vista).
    """
    event = models.ForeignKey(
        Event,
        related_name="inscripciones",
        on_delete=models.CASCADE,
    )
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="inscripciones",
        on_delete=models.CASCADE,
    )
    cantidad = models.PositiveIntegerField(default=1)
    creado_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("event", "usuario")
        verbose_name = "Inscripción"
        verbose_name_plural = "Inscripciones"

    def __str__(self):
        return f"{self.usuario} - {self.event} ({self.cantidad})"
