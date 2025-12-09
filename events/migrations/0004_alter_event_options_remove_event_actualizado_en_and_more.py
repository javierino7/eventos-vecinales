from django.db import migrations

DROP_COLUMNS_SQL = """
-- eliminar columnas si existen, con SQL dinámico
SET @db := DATABASE();

-- actualizado_en
SET @cnt := (SELECT COUNT(*) FROM INFORMATION_SCHEMA.COLUMNS
             WHERE TABLE_SCHEMA=@db AND TABLE_NAME='events_event' AND COLUMN_NAME='actualizado_en');
SET @sql := IF(@cnt>0, 'ALTER TABLE `events_event` DROP COLUMN `actualizado_en`', 'SELECT 1');
PREPARE s FROM @sql; EXECUTE s; DEALLOCATE PREPARE s;

-- creado_en
SET @cnt := (SELECT COUNT(*) FROM INFORMATION_SCHEMA.COLUMNS
             WHERE TABLE_SCHEMA=@db AND TABLE_NAME='events_event' AND COLUMN_NAME='creado_en');
SET @sql := IF(@cnt>0, 'ALTER TABLE `events_event` DROP COLUMN `creado_en`', 'SELECT 1');
PREPARE s FROM @sql; EXECUTE s; DEALLOCATE PREPARE s;

-- cupos_totales
SET @cnt := (SELECT COUNT(*) FROM INFORMATION_SCHEMA.COLUMNS
             WHERE TABLE_SCHEMA=@db AND TABLE_NAME='events_event' AND COLUMN_NAME='cupos_totales');
SET @sql := IF(@cnt>0, 'ALTER TABLE `events_event` DROP COLUMN `cupos_totales`', 'SELECT 1');
PREPARE s FROM @sql; EXECUTE s; DEALLOCATE PREPARE s;

-- fecha
SET @cnt := (SELECT COUNT(*) FROM INFORMATION_SCHEMA.COLUMNS
             WHERE TABLE_SCHEMA=@db AND TABLE_NAME='events_event' AND COLUMN_NAME='fecha');
SET @sql := IF(@cnt>0, 'ALTER TABLE `events_event` DROP COLUMN `fecha`', 'SELECT 1');
PREPARE s FROM @sql; EXECUTE s; DEALLOCATE PREPARE s;

-- hora_fin
SET @cnt := (SELECT COUNT(*) FROM INFORMATION_SCHEMA.COLUMNS
             WHERE TABLE_SCHEMA=@db AND TABLE_NAME='events_event' AND COLUMN_NAME='hora_fin');
SET @sql := IF(@cnt>0, 'ALTER TABLE `events_event` DROP COLUMN `hora_fin`', 'SELECT 1');
PREPARE s FROM @sql; EXECUTE s; DEALLOCATE PREPARE s;

-- hora_inicio
SET @cnt := (SELECT COUNT(*) FROM INFORMATION_SCHEMA.COLUMNS
             WHERE TABLE_SCHEMA=@db AND TABLE_NAME='events_event' AND COLUMN_NAME='hora_inicio');
SET @sql := IF(@cnt>0, 'ALTER TABLE `events_event` DROP COLUMN `hora_inicio`', 'SELECT 1');
PREPARE s FROM @sql; EXECUTE s; DEALLOCATE PREPARE s;
"""

ADD_COLUMNS_SQL = """
SET @db := DATABASE();

-- cupos
SET @cnt := (SELECT COUNT(*) FROM INFORMATION_SCHEMA.COLUMNS
             WHERE TABLE_SCHEMA=@db AND TABLE_NAME='events_event' AND COLUMN_NAME='cupos');
SET @sql := IF(@cnt=0, 'ALTER TABLE `events_event` ADD COLUMN `cupos` int unsigned NOT NULL DEFAULT 0', 'SELECT 1');
PREPARE s FROM @sql; EXECUTE s; DEALLOCATE PREPARE s;

-- lugar
SET @cnt := (SELECT COUNT(*) FROM INFORMATION_SCHEMA.COLUMNS
             WHERE TABLE_SCHEMA=@db AND TABLE_NAME='events_event' AND COLUMN_NAME='lugar');
SET @sql := IF(@cnt=0, 'ALTER TABLE `events_event` ADD COLUMN `lugar` varchar(200) NOT NULL DEFAULT ""', 'SELECT 1');
PREPARE s FROM @sql; EXECUTE s; DEALLOCATE PREPARE s;

-- inicio
SET @cnt := (SELECT COUNT(*) FROM INFORMATION_SCHEMA.COLUMNS
             WHERE TABLE_SCHEMA=@db AND TABLE_NAME='events_event' AND COLUMN_NAME='inicio');
SET @sql := IF(@cnt=0, 'ALTER TABLE `events_event` ADD COLUMN `inicio` datetime(6) NOT NULL DEFAULT "2000-01-01 00:00:00.000000"', 'SELECT 1');
PREPARE s FROM @sql; EXECUTE s; DEALLOCATE PREPARE s;

-- fin
SET @cnt := (SELECT COUNT(*) FROM INFORMATION_SCHEMA.COLUMNS
             WHERE TABLE_SCHEMA=@db AND TABLE_NAME='events_event' AND COLUMN_NAME='fin');
SET @sql := IF(@cnt=0, 'ALTER TABLE `events_event` ADD COLUMN `fin` datetime(6) NOT NULL DEFAULT "2000-01-01 00:00:00.000000"', 'SELECT 1');
PREPARE s FROM @sql; EXECUTE s; DEALLOCATE PREPARE s;

-- estado
SET @cnt := (SELECT COUNT(*) FROM INFORMATION_SCHEMA.COLUMNS
             WHERE TABLE_SCHEMA=@db AND TABLE_NAME='events_event' AND COLUMN_NAME='estado');
SET @sql := IF(@cnt=0, 'ALTER TABLE `events_event` ADD COLUMN `estado` varchar(10) NOT NULL DEFAULT "pendiente"', 'SELECT 1');
PREPARE s FROM @sql; EXECUTE s; DEALLOCATE PREPARE s;
"""

class Migration(migrations.Migration):
    dependencies = [
        ('events', '0002_alter_event_options_event_actualizado_en_and_more'),
    ]

    operations = [
        migrations.RunSQL(sql=DROP_COLUMNS_SQL, reverse_sql=migrations.RunSQL.noop),
        migrations.RunSQL(sql=ADD_COLUMNS_SQL, reverse_sql=migrations.RunSQL.noop),
        # OJO: no tocamos M2M asistentes aquí (evita el error de incompatibilidad).
    ]
