# events/migrations/0006_add_estado_to_event.py
from django.db import migrations, models

def set_default_estado(apps, schema_editor):
    # Asegura que filas existentes queden con 'activo'
    schema_editor.execute("UPDATE events_event SET estado = 'activo' WHERE estado IS NULL")

class Migration(migrations.Migration):

    dependencies = [
        ("events", "0005_alter_rsvp_unique_together"),  # ajusta si tu último número difiere
    ]

    operations = [
        migrations.AddField(
            model_name="event",
            name="estado",
            field=models.CharField(choices=[("activo", "Activo"), ("cancelado", "Cancelado"), ("finalizado", "Finalizado")],
                                   default="activo", max_length=20, db_index=True),
        ),
        migrations.RunPython(set_default_estado, reverse_code=migrations.RunPython.noop),
    ]
