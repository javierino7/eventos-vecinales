from django.db import migrations

migrations.SeparateDatabaseAndState(
    database_operations=[
        migrations.RunSQL(
            sql="ALTER TABLE `events_event` DROP COLUMN IF EXISTS `actualizado_en`;",
            reverse_sql=migrations.RunSQL.noop,
        ),
    ],
    state_operations=[
        migrations.RemoveField(model_name='event', name='actualizado_en'),
    ],
),
