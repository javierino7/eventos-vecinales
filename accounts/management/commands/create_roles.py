# accounts/management/commands/create_roles.py
from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from events.models import Event, RSVP

class Command(BaseCommand):
    help = "Crea grupos de roles y asigna permisos"

    def handle(self, *args, **options):
        # ContentTypes
        event_ct = ContentType.objects.get_for_model(Event)
        rsvp_ct = ContentType.objects.get_for_model(RSVP)

        # Permisos base de Event
        perms_event = {
            "add_event": Permission.objects.get(codename="add_event", content_type=event_ct),
            "change_event": Permission.objects.get(codename="change_event", content_type=event_ct),
            "delete_event": Permission.objects.get(codename="delete_event", content_type=event_ct),
            "view_event": Permission.objects.get(codename="view_event", content_type=event_ct),
            "approve_event": Permission.objects.get(codename="approve_event", content_type=event_ct),
            "view_pending_events": Permission.objects.get(codename="view_pending_events", content_type=event_ct),
        }

        # Permisos base de RSVP
        perms_rsvp = {
            "add_rsvp": Permission.objects.get(codename="add_rsvp", content_type=rsvp_ct),
            "change_rsvp": Permission.objects.get(codename="change_rsvp", content_type=rsvp_ct),
            "delete_rsvp": Permission.objects.get(codename="delete_rsvp", content_type=rsvp_ct),
            "view_rsvp": Permission.objects.get(codename="view_rsvp", content_type=rsvp_ct),
        }

        # Grupo: vecino
        vecino, _ = Group.objects.get_or_create(name="vecino")
        vecino_perms = [
            perms_event["view_event"],
            perms_event["add_event"],             # puede crear (queda pendiente)
            perms_rsvp["add_rsvp"],              # confirmar asistencia
            perms_rsvp["change_rsvp"],           # cancelar asistencia
            perms_rsvp["view_rsvp"],
        ]
        vecino.permissions.set(vecino_perms)

        # Grupo: moderador
        moderador, _ = Group.objects.get_or_create(name="moderador")
        moderador_perms = [
            perms_event["view_event"],
            perms_event["view_pending_events"],
            perms_event["approve_event"],        # aprobar/rechazar
            perms_event["change_event"],         # editar por moderación
            perms_rsvp["view_rsvp"],
            perms_rsvp["change_rsvp"],
        ]
        moderador.permissions.set(moderador_perms)

        # Grupo: administrador
        administrador, _ = Group.objects.get_or_create(name="administrador")
        # Admin: todos los permisos de Event y RSVP
        all_event_perms = Permission.objects.filter(content_type=event_ct)
        all_rsvp_perms = Permission.objects.filter(content_type=rsvp_ct)
        administrador.permissions.set(list(all_event_perms) + list(all_rsvp_perms))

        self.stdout.write(self.style.SUCCESS("Grupos y permisos creados/asignados."))
