import uuid
from datetime import datetime
from enum import Enum

from django.db import models, transaction
from django.conf import settings

from external.migration import DatabaseMigration


class FIELD_TYPES(Enum):   # A subclass of Enum
    CHAR = "char"
    BOOLEAN = "bool"
    INTEGER = 'int'
    DECIMAL = 'dec'
    DATE = "timestamp"
    UUID = "UUID"
    SERIAL = "SERIAL"

    def __str__(self):
        return self.value


class Solution(models.Model):
    """
    Solution model. This is the main solution to which the platform will serve. (SAGER)
    """
    name = models.CharField(max_length=30, unique=True)


class App(models.Model):
    """
    app model
    """
    name = models.CharField(max_length=30)
    solution = models.ForeignKey(Solution, on_delete=models.CASCADE, related_name='apps')


class Entity(models.Model):
    """
    Entity model. This is the Entity that will be used in the solution. (USINA)
    """
    solution = models.ForeignKey(Solution, on_delete=models.CASCADE, related_name='entities')
    name = models.CharField(max_length=30)
    table = models.CharField(max_length=30, unique=True)

    SCHEMA = {
        'id': FIELD_TYPES.INTEGER,
        'date_created': FIELD_TYPES.DATE
    }

    def make_migration(self):
        first = not self.migrations.exists()
        fields = self.fields.filter(migration__isnull=True)

        with transaction.atomic():
            if fields.exists():
                migration = Migration.objects.create(entity=self, first=first)
                fields.update(migration=migration)
                return migration

    def save(self, *args, **kwargs):
        with transaction.atomic():
            super(Entity, self).save(*args, **kwargs)
            for field, field_type in self.SCHEMA.items():
                Field.objects.create(
                    entity=self, name=field, field_type=field_type)


class Migration(models.Model):
    """
    Domain migration
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    date_created = models.DateTimeField(auto_now=True)
    date_executed = models.DateTimeField(null=True)
    entity = models.ForeignKey(Entity, on_delete=models.CASCADE, related_name='migrations')
    first = models.BooleanField(default=False)

    @property
    def history_table(self):
        return f'{self.entity.table}_history'

    def _create_history_table(self, migration):
        """
        base create history table command.

        returns:
        migration command which creates the entity history table
        with the following columns:
            - uuid primary key named version_id,
            - uuid foreign key named id referencing the entity itself,
            - date_created to keep the version creation date.
        """
        return migration.create_table(self.history_table, 'entities')\
            .with_column(
                name='version_id',
                field_type=FIELD_TYPES.UUID,
                primary_key=True,
                default='uuid_generate_v4()'
            ).with_column(
                name='id',
                field_type=FIELD_TYPES.UUID,
                references=(self.entity.table, 'id'),
                required=True,
            ).with_column(
                name='date_created',
                required=True,
                field_type=FIELD_TYPES.DATE,)

    def _create_table(self, migration):
        """
        base create table command.

        returns:
        migration command which creates the entity table with the following
        columns:
            - primary key named id.
            - date_created to keep the version creation date.
        """
        return migration.create_table(self.entity.table, 'entities')\
            .with_column(
                name='id',
                field_type=FIELD_TYPES.UUID,
                primary_key=True,
                default='uuid_generate_v4()'
            ).with_column(
                name='date_created',
                field_type=FIELD_TYPES.DATE,
                required=True,
                default='NOW()')

    def create_tables(self):
        """
        creates entity table and history table.
        """
        migration = DatabaseMigration(settings.MIGRATION_DIALECT)
        table = self._create_table(migration)
        history_table = self._create_history_table(migration)

        for field in self.fields.exclude(name__in=(Entity.SCHEMA.keys())):
            table = table.with_column(field.name, field.field_type)
            history_table = history_table.with_column(field.name, field.field_type)

        return table, history_table,

    def alter_tables(self):
        db_migration = DatabaseMigration(settings.MIGRATION_DIALECT)
        table = db_migration.alter_table(self.entity.table)
        table_history = db_migration.alter_table(self.history_table)

        for field in self.fields.all():
            table = table.add_column(field.name, field.field_type)
            table_history = table_history.add_column(field.name, field.field_type)

        return table, table_history,

    def run(self):
        """apply current migration
        """
        from .tasks import apply_model_migration
        apply_model_migration.delay(self.id)


class Field(models.Model):
    """
    field model
    """
    name = models.CharField(max_length=30)
    entity = models.ForeignKey(Entity, on_delete=models.CASCADE, related_name='fields')
    migration = models.ForeignKey(Migration, on_delete=models.CASCADE, related_name='fields', null=True)
    field_type = models.CharField(
        max_length=12,
        choices=[(field, field.value) for field in FIELD_TYPES])


class EntityMap(models.Model):
    """
    Map model
    """
    app = models.ForeignKey(App, on_delete=models.CASCADE, related_name='maps')
    entity = models.ForeignKey(Entity, on_delete=models.CASCADE, related_name='maps')
    name = models.CharField(max_length=30)


class MappedField(models.Model):
    """
    Mapped field model
    """
    entity_map = models.ForeignKey(EntityMap, on_delete=models.CASCADE, related_name='fields')
    field = models.ForeignKey(Field, on_delete=models.CASCADE, related_name='mappings')
    alias = models.CharField(max_length=30)

