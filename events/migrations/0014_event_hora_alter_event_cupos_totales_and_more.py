# events/migrations/0014_event_hora_alter_event_cupos_totales_and_more.py
# Ajuste: NO volvemos a crear la columna "hora", solo actualizamos campos existentes.

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0013_alter_event_options_event_hora_event_precio_entrada_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='cupos_totales',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='event',
            name='solo_mayores_18',
            field=models.BooleanField(
                default=True,
                help_text='Si está marcado, solo pueden asistir personas mayores de 18 años.',
            ),
        ),
    ]
