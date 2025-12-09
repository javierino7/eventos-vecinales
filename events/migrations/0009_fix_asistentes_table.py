from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        # Esta es la ÚLTIMA migración que tienes aplicada
        ('events', '0008_alter_event_options_rename_cupos_event_cupos_totales_and_more'),
    ]

    operations = [
        migrations.RunSQL(
            sql="""
                CREATE TABLE IF NOT EXISTS `events_event_asistentes` (
                    `id` bigint AUTO_INCREMENT NOT NULL PRIMARY KEY,
                    `event_id` bigint NOT NULL,
                    `user_id` bigint NOT NULL,
                    CONSTRAINT `events_event_asistentes_event_id_fk`
                        FOREIGN KEY (`event_id`)
                        REFERENCES `events_event` (`id`)
                        ON DELETE CASCADE,
                    CONSTRAINT `events_event_asistentes_user_id_fk`
                        FOREIGN KEY (`user_id`)
                        REFERENCES `accounts_user` (`id`)
                        ON DELETE CASCADE,
                    UNIQUE KEY `events_event_asistentes_event_user_uniq` (`event_id`, `user_id`)
                ) ENGINE=InnoDB;
            """,
            reverse_sql="DROP TABLE IF EXISTS `events_event_asistentes`;",
        ),
    ]
