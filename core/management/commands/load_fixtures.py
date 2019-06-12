from django.core.management.base import BaseCommand
from django.core.management import call_command
from core import models

from core.tasks import apply_model_migration


class Command(BaseCommand):
    def handle(self, **options):
        call_command('loaddata', './core/tests/fixtures/test_data.json')
        usina = models.Entity.objects.get(pk=1)
        migration = usina.make_migration()
        __import__('ipdb').set_trace()
        apply_model_migration(migration.id)

