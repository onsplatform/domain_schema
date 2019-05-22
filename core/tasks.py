from datetime import datetime

from django.db import connection, transaction

from domain_schema.celery import app
from .models import Migration


@app.task(trail=True)
def apply_model_migration(migration_id):
    migration = Migration.objects.get(pk=migration_id)
    commands = migration.create_tables if migration.first else migration.alter_tables
    command, history_command = commands()

    command = command.build()
    history_command = history_command.build()

    with transaction.atomic():
        with connection.cursor() as cursor:
            cursor.execute(command)
            cursor.execute(history_command)

        migration.date_executed = datetime.now()
        migration.save()

    return {
        'command': command,
        'history_command': history_command,
        'migration': migration.id,
    }
