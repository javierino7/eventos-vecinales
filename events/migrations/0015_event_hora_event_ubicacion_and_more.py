# Generated manually para evitar columnas duplicadas

from django.db import migrations, models
from django.conf import settings
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("events", "0014_event_hora_alter_event_cupos_totales_and_more"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        # Solo ajustamos el campo solo_mayores_18 según tu models.py actual
        migrations.AlterField(
            model_name="event",
            name="solo_mayores_18",
            field=models.BooleanField(
                default=True,
                help_text=(
                    "Si está marcado, solo pueden asistir personas "
                    "mayores de 18 años."
                ),
            ),
        ),

        # Creamos la tabla de inscripciones (EventRegistration)
        migrations.CreateModel(
            name="EventRegistration",
            fields=[
                ("id", models.BigAutoField(auto_created=True,
                                           primary_key=True,
                                           serialize=False,
                                           verbose_name="ID")),
                ("cantidad", models.PositiveIntegerField(default=1)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "evento",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="inscripciones",
                        to="events.event",
                    ),
                ),
                (
                    "usuario",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="inscripciones_eventos",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "unique_together": {("evento", "usuario")},
            },
        ),
    ]
