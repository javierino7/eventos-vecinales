from django.db import migrations, models
from django.conf import settings

class Migration(migrations.Migration):
    dependencies = [
        ('events', '0005_merge_conflict'),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            # NO hacemos cambios en la DB acá porque la 0004 (RunSQL) ya lo hizo.
            database_operations=[],
            state_operations=[
                # 1) Quitar del estado los campos viejos (no existen en DB porque la 0004 los borró)
                migrations.RemoveField(model_name='event', name='actualizado_en'),
                migrations.RemoveField(model_name='event', name='creado_en'),
                migrations.RemoveField(model_name='event', name='cupos_totales'),
                migrations.RemoveField(model_name='event', name='fecha'),
                migrations.RemoveField(model_name='event', name='hora_inicio'),
                migrations.RemoveField(model_name='event', name='hora_fin'),

                # 2) Agregar al estado los campos nuevos (ya existen en DB por la 0004)
                migrations.AddField(
                    model_name='event',
                    name='cupos',
                    field=models.PositiveIntegerField(default=0),
                ),
                migrations.AddField(
                    model_name='event',
                    name='lugar',
                    field=models.CharField(max_length=200),
                ),
                migrations.AddField(
                    model_name='event',
                    name='inicio',
                    field=models.DateTimeField(),
                ),
                migrations.AddField(
                    model_name='event',
                    name='fin',
                    field=models.DateTimeField(),
                ),
                migrations.AddField(
                    model_name='event',
                    name='estado',
                    field=models.CharField(
                        max_length=10,
                        default='pendiente',
                        choices=[('pendiente', 'Pendiente'), ('aprobado', 'Aprobado'), ('rechazado', 'Rechazado')],
                    ),
                ),

                # 3) Asegurar related_name correcto del M2M en el estado (DB no cambia)
                migrations.AlterField(
                    model_name='event',
                    name='asistentes',
                    field=models.ManyToManyField(
                        to=settings.AUTH_USER_MODEL,
                        blank=True,
                        related_name='eventos_asistidos',
                    ),
                ),

                # 4) Orden por 'inicio'
                migrations.AlterModelOptions(
                    name='event',
                    options={'ordering': ['inicio']},
                ),
            ],
        ),
    ]
