from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.db import connection

from core import models
from core.tasks import apply_model_migration


class Command(BaseCommand):
    def handle(self, **options):
        call_command('loaddata', './core/tests/fixtures/test_data.json')
        usina = models.Entity.objects.get(pk=1)
        migration = usina.make_migration()
        apply_model_migration(migration.id)

        with connection.cursor() as cursor:
            cursor.execute("INSERT INTO entities.sager_usina (nome) VALUES ('ITAIPU');")
            cursor.execute("UPDATE entities.sager_usina SET nome = 'ITAEPU';")
            cursor.execute("UPDATE entities.sager_usina SET nome = 'ITAUPU';")

