from django.db import migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ("events", "0015_event_hora_event_ubicacion_and_more"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        # Opciones del modelo EventRegistration
        migrations.AlterModelOptions(
            name="eventregistration",
            options={
                "verbose_name": "Inscripción",
                "verbose_name_plural": "Inscripciones",
                "ordering": ("-creado_en",),
            },
        ),

        # IMPORTANTE:
        # Estos RenameField se aplican SOLO al "estado" de Django,
        # NO ejecutan ALTER TABLE en la base de datos.
        migrations.SeparateDatabaseAndState(
            database_operations=[],
            state_operations=[
                migrations.RenameField(
                    model_name="eventregistration",
                    old_name="created_at",
                    new_name="creado_en",
                ),
                migrations.RenameField(
                    model_name="eventregistration",
                    old_name="evento",
                    new_name="event",
                ),
                migrations.RenameField(
                    model_name="eventregistration",
                    old_name="usuario",
                    new_name="user",
                ),
            ],
        ),

        # Un usuario solo puede tener UNA inscripción por evento
        migrations.AlterUniqueTogether(
            name="eventregistration",
            unique_together={("event", "user")},
        ),
    ]
