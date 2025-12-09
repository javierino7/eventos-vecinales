# events/views.py

from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q, Sum
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    TemplateView,
    UpdateView,
)

from .forms import EventForm, CheckoutForm
from .models import Event, Inscripcion


# ---------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------
def es_admin_o_moderador(user):
    """
    Retorna True si el usuario tiene permisos de administración de eventos.
    Considera:
      - superusuario
      - staff
      - rol == 'administrador' / 'admin' / 'moderador'
    """
    if not user.is_authenticated:
        return False

    rol = getattr(user, "rol", "")

    return (
        getattr(user, "is_superuser", False)
        or getattr(user, "is_staff", False)
        or rol in ["administrador", "admin", "moderador"]
    )


# ---------------------------------------------------------------------
# Listado / detalle
# ---------------------------------------------------------------------
class EventListView(ListView):
    model = Event
    template_name = "events/event_list.html"
    context_object_name = "eventos"

    def get_queryset(self):
        qs = (
            Event.objects.filter(estado=Event.ESTADO_APROBADO)
            .order_by("fecha_inicio", "hora_inicio", "titulo")
        )

        q = self.request.GET.get("q", "").strip()
        localidad = self.request.GET.get("localidad", "").strip()
        solo_mis_eventos = self.request.GET.get("solo_mis_eventos")

        if q:
            qs = qs.filter(
                Q(titulo__icontains=q)
                | Q(descripcion__icontains=q)
                | Q(localidad__icontains=q)
                | Q(lugar__icontains=q)
            )

        if localidad:
            qs = qs.filter(localidad__iexact=localidad)

        if solo_mis_eventos and self.request.user.is_authenticated:
            qs = qs.filter(inscripciones__usuario=self.request.user).distinct()

        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        localidades = (
            Event.objects.exclude(localidad__isnull=True)
            .exclude(localidad__exact="")
            .values_list("localidad", flat=True)
            .distinct()
            .order_by("localidad")
        )
        context["localidades_disponibles"] = localidades
        return context


class EventDetailView(DetailView):
    model = Event
    template_name = "events/event_detail.html"
    context_object_name = "evento"

    def get_queryset(self):
        qs = Event.objects.all()
        # Usuarios normales sólo ven eventos aprobados
        if not es_admin_o_moderador(self.request.user):
            qs = qs.filter(estado=Event.ESTADO_APROBADO)
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        evento = self.object
        inscripcion = None

        if self.request.user.is_authenticated:
            inscripcion = Inscripcion.objects.filter(
                event=evento,
                usuario=self.request.user,
            ).first()

        ctx["inscripcion_actual"] = inscripcion
        ctx["ya_inscrito"] = inscripcion is not None

        # ---- chequeo de edad para eventos +18 ----
        puede_por_edad = True
        user = self.request.user

        if evento.solo_mayores_18:
            puede_por_edad = False  # por defecto NO
            if user.is_authenticated:
                fecha_nac = (
                    getattr(user, "fecha_nacimiento", None)
                    or getattr(user, "birth_date", None)
                    or getattr(user, "fecha_nac", None)
                )
                if fecha_nac:
                    hoy = timezone.now().date()
                    edad = (
                        hoy.year
                        - fecha_nac.year
                        - (
                            (hoy.month, hoy.day)
                            < (fecha_nac.month, fecha_nac.day)
                        )
                    )
                    if edad >= 18:
                        puede_por_edad = True

        ctx["puede_inscribirse_por_edad"] = puede_por_edad
        return ctx


# ---------------------------------------------------------------------
# CRUD eventos (creador / admin / moderador)
# ---------------------------------------------------------------------
class DueñoEventoMixin(UserPassesTestMixin):
    """
    Mixin para permitir edición/eliminación solo al creador o admin/mod.
    """

    def test_func(self):
        obj = self.get_object()
        user = self.request.user
        if not user.is_authenticated:
            return False
        if es_admin_o_moderador(user):
            return True
        return obj.creado_por_id == user.id


class EventCreateView(LoginRequiredMixin, CreateView):
    model = Event
    template_name = "events/event_form.html"
    form_class = EventForm
    success_url = reverse_lazy("events:mis_eventos")

    def form_valid(self, form):
        form.instance.creado_por = self.request.user
        # al crear, que quede pendiente de aprobación si no viene nada
        if not form.instance.estado:
            form.instance.estado = Event.ESTADO_PENDIENTE
        messages.success(
            self.request,
            "Tu evento fue creado correctamente y está pendiente de aprobación.",
        )
        return super().form_valid(form)


class EventUpdateView(LoginRequiredMixin, DueñoEventoMixin, UpdateView):
    model = Event
    template_name = "events/event_form.html"
    form_class = EventForm

    def get_success_url(self):
        messages.success(self.request, "El evento se actualizó correctamente.")
        return reverse_lazy("events:detalle", kwargs={"pk": self.object.pk})


class EventDeleteView(LoginRequiredMixin, DueñoEventoMixin, DeleteView):
    model = Event
    template_name = "events/event_confirm_delete.html"
    success_url = reverse_lazy("events:mis_eventos")

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "El evento se eliminó correctamente.")
        return super().delete(request, *args, **kwargs)


# ---------------------------------------------------------------------
# Mis eventos / panel admin
# ---------------------------------------------------------------------
class MisEventosListView(LoginRequiredMixin, ListView):
    """
    Lista de eventos a los que el usuario está inscrito.
    """
    template_name = "events/mis_eventos.html"
    context_object_name = "inscripciones"

    def get_queryset(self):
        return (
            Inscripcion.objects.select_related("event")
            .filter(usuario=self.request.user)
            .order_by("-creado_en")
        )


@method_decorator(user_passes_test(es_admin_o_moderador), name="dispatch")
class AdminPanelView(TemplateView):
    """
    Panel para admin/moderador con métricas y eventos pendientes.
    """
    template_name = "events/panel_admin.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        todos = Event.objects.all().order_by("-creado_en")

        ctx["total_eventos"] = todos.count()
        ctx["eventos_aprobados"] = todos.filter(
            estado=Event.ESTADO_APROBADO
        ).count()
        ctx["eventos_rechazados"] = todos.filter(
            estado=Event.ESTADO_RECHAZADO
        ).count()
        ctx["eventos_pendientes"] = todos.filter(
            estado=Event.ESTADO_PENDIENTE
        )

        # para la tabla de "últimos eventos creados"
        ctx["eventos_recientes"] = todos[:10]

        return ctx


@user_passes_test(es_admin_o_moderador)
def cambiar_estado_evento(request, pk, nuevo_estado):
    """
    Vista rápida para aprobar / rechazar / volver a pendiente un evento.
    """
    evento = get_object_or_404(Event, pk=pk)

    if nuevo_estado not in [
        Event.ESTADO_PENDIENTE,
        Event.ESTADO_APROBADO,
        Event.ESTADO_RECHAZADO,
    ]:
        messages.error(request, "Estado no válido.")
        return redirect("events:panel_admin")

    evento.estado = nuevo_estado
    evento.save(update_fields=["estado"])
    messages.success(request, f"El estado del evento se actualizó a: {nuevo_estado}.")
    return redirect("events:panel_admin")


# ---------------------------------------------------------------------
# Checkout / inscripción
# ---------------------------------------------------------------------
@login_required
def asistir(request, pk):
    """
    Paso de 'checkout' de entradas / inscripción al evento.
    """
    evento = get_object_or_404(Event, pk=pk)

    # --- bloqueo por edad para eventos +18 ---
    if evento.solo_mayores_18:
        user = request.user
        fecha_nac = (
            getattr(user, "fecha_nacimiento", None)
            or getattr(user, "birth_date", None)
            or getattr(user, "fecha_nac", None)
        )
        if not fecha_nac:
            messages.error(
                request,
                (
                    "Este evento es solo para mayores de 18 años. "
                    "Actualiza tu fecha de nacimiento en el perfil si corresponde."
                ),
            )
            return redirect("events:detalle", pk=evento.pk)

        hoy = timezone.now().date()
        edad = (
            hoy.year
            - fecha_nac.year
            - ((hoy.month, hoy.day) < (fecha_nac.month, fecha_nac.day))
        )
        if edad < 18:
            messages.error(
                request,
                "No puedes inscribirte en este evento porque es solo para mayores de 18 años.",
            )
            return redirect("events:detalle", pk=evento.pk)

    # si no está aprobado o ya terminó, no permitimos
    if evento.estado != Event.ESTADO_APROBADO or evento.esta_finalizado:
        messages.error(
            request, "Este evento no está disponible para nuevas inscripciones."
        )
        return redirect("events:detalle", pk=evento.pk)

    # cantidad desde GET o POST (viene del detalle)
    raw_cantidad = request.GET.get("cantidad") or request.POST.get("cantidad") or "1"
    try:
        cantidad = int(raw_cantidad)
    except (TypeError, ValueError):
        cantidad = 1

    # límite 1–5
    if cantidad < 1:
        cantidad = 1
    if cantidad > 5:
        cantidad = 5

    # buscamos si ya tiene inscripción
    inscripcion_actual = Inscripcion.objects.filter(
        event=evento, usuario=request.user
    ).first()

    # cálculo de cupos restantes sin contar al usuario actual (si ya está inscrito)
    cupos_restantes = None
    if evento.cupos_totales is not None:
        qs = evento.inscripciones.all()
        if inscripcion_actual:
            qs = qs.exclude(pk=inscripcion_actual.pk)

        usados_por_otros = qs.aggregate(total=Sum("cantidad"))["total"] or 0
        cupos_restantes = max(evento.cupos_totales - usados_por_otros, 0)
        if cantidad > cupos_restantes:
            cantidad = max(cupos_restantes, 0)

    if request.method == "POST":
        form = CheckoutForm(request.POST)

        if not form.is_valid():
            total = (evento.precio_entrada or 0) * cantidad
            context = {
                "event": evento,
                "evento": evento,
                "form": form,
                "cantidad": cantidad,
                "total": total,
                "ya_inscrito": inscripcion_actual is not None,
                "inscripcion_actual": inscripcion_actual,
                "cupos_restantes": cupos_restantes,
            }
            return render(request, "events/event_checkout.html", context)

        # doble chequeo
        if evento.esta_finalizado:
            messages.error(request, "El evento ya finalizó.")
            return redirect("events:detalle", pk=evento.pk)

        if cupos_restantes is not None and cantidad > cupos_restantes:
            messages.error(
                request,
                f"Solo quedan {cupos_restantes} cupos disponibles para este evento.",
            )
            return redirect("events:detalle", pk=evento.pk)

        # actualizar o crear inscripción (solo cantidad)
        if inscripcion_actual:
            inscripcion_actual.cantidad = cantidad
            inscripcion_actual.save(update_fields=["cantidad"])
        else:
            if cupos_restantes is not None and cantidad == 0:
                messages.error(
                    request, "No quedan cupos disponibles para este evento."
                )
                return redirect("events:detalle", pk=evento.pk)

            Inscripcion.objects.create(
                event=evento,
                usuario=request.user,
                cantidad=cantidad,
            )

        messages.success(request, "Tu asistencia fue registrada correctamente.")
        return redirect("events:checkout_exito", pk=evento.pk)

    else:
        # GET
        initial = {
            "nombre": request.user.get_full_name() or request.user.username,
            "email": request.user.email,
        }
        form = CheckoutForm(initial=initial)

    total = (evento.precio_entrada or 0) * cantidad

    context = {
        "event": evento,
        "evento": evento,
        "form": form,
        "cantidad": cantidad,
        "total": total,
        "ya_inscrito": inscripcion_actual is not None,
        "inscripcion_actual": inscripcion_actual,
        "cupos_restantes": cupos_restantes,
    }
    return render(request, "events/event_checkout.html", context)


@login_required
def checkout_exito(request, pk):
    """
    Pantalla de 'pago/inscripción exitosa'.
    """
    evento = get_object_or_404(Event, pk=pk)
    inscripcion = Inscripcion.objects.filter(
        event=evento, usuario=request.user
    ).first()

    if not inscripcion:
        messages.error(
            request, "No tienes una inscripción registrada para este evento."
        )
        return redirect("events:detalle", pk=evento.pk)

    cantidad = inscripcion.cantidad
    total = (evento.precio_entrada or 0) * cantidad

    context = {
        "event": evento,
        "evento": evento,
        "inscripcion": inscripcion,
        "cantidad": cantidad,
        "total": total,
    }
    return render(request, "events/event_checkout_exito.html", context)
