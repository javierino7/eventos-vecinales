from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0016_alter_eventregistration_options_and_more'),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            database_operations=[],
            state_operations=[
                migrations.AddField(
                    model_name='event',
                    name='hora',
                    field=models.TimeField(blank=True, null=True),
                ),
                migrations.AddField(
                    model_name='event',
                    name='ubicacion',
                    field=models.CharField(
                        max_length=255,
                        null=True,
                        blank=True,
                    ),
                ),
            ],
        ),

        migrations.AlterField(
            model_name='event',
            name='solo_mayores_18',
            field=models.BooleanField(
                default=False,
                help_text='Si está marcado, solo pueden asistir personas mayores de 18 años.',
            ),
        ),

        migrations.CreateModel(
            name='Inscripcion',
            fields=[
                (
                    'id',
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID',
                    ),
                ),
                ('cantidad', models.PositiveIntegerField(default=1)),
                ('creado_en', models.DateTimeField(auto_now_add=True)),
                (
                    'event',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name='inscripciones',
                        to='events.event',
                    ),
                ),
                (
                    'usuario',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name='inscripciones',
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                'verbose_name': 'Inscripción',
                'verbose_name_plural': 'Inscripciones',
                'unique_together': {('event', 'usuario')},
            },
        ),

        migrations.DeleteModel(
            name='EventRegistration',
        ),
    ]
