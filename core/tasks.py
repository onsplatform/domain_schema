from datetime import datetime

from django.db import connection, transaction

from domain_schema.celery import app
from .models import Migration


@app.task(trail=True)
def apply_model_migration(migration_id):
    migration = Migration.objects.get(pk=migration_id)
    command = migration._create_table if migration.first else migration._alter_table
    command = command().build()
    execution_result = None

    with transaction.atomic():
        with connection.cursor() as cursor:
            exec_result = cursor.execute(command)

        migration.date_executed = datetime.now()
        migration.save()

    return {
        'command': command,
        'migration': migration.id,
        'execution_result': execution_result,
    }


