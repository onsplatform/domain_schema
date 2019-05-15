import uuid
from datetime import datetime
from enum import Enum

from django.db import models
from django.conf import settings

from external.migration import DatabaseMigration


class FIELD_TYPES(Enum):   # A subclass of Enum
    CHAR = "char"
    BOOLEAN = "bool"
    INTEGER = 'int'
    DECIMAL = 'dec'

    def __str__(self):
        return self.value


class Solution(models.Model):
    """
    Solution model. This is the main solution to which the platform will serve. (SAGER)
    """
    name = models.CharField(max_length=30)


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
    table = models.CharField(max_length=30)

    def make_migration(self):
        first = not self.migrations.exists()
        migration = Migration.objects.create(entity=self, first=first)
        self.fields.filter(migration__isnull=True)\
            .update(migration=migration)
        return migration


class Migration(models.Model):
    """
    Domain migration
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    date_created = models.DateTimeField(auto_now=True)
    date_executed = models.DateTimeField(null=True)
    entity = models.ForeignKey(Entity, on_delete=models.CASCADE, related_name='migrations')
    first = models.BooleanField(default=False)

    def _create_table(self):
        db_migration = DatabaseMigration(settings.MIGRATION_DIALECT)
        table = db_migration.create_table(self.entity.table) \
                    .with_column('id', FIELD_TYPES.INTEGER, primary_key=True)

        for field in self.fields.all():
            table = table.with_column(field.name, field.field_type)

        return table

    def _alter_table(self):
        db_migration = DatabaseMigration(settings.MIGRATION_DIALECT)
        table = db_migration.alter_table(self.entity.table)

        for field in self.fields.all():
            table = table.add_column(field.name, field.field_type)

        return table

    def run(self):
        """apply current migration

        :arg1: TODO
        :returns: TODO

        """
        command = (self._create_table if self.first else self._alter_table)()
        command = command.build()

        self.date_executed = datetime.now()
        self.save()

class Field(models.Model):
    """
    field model
    """
    name = models.CharField(max_length=30)
    entity = models.ForeignKey(Entity, on_delete=models.CASCADE, related_name='fields')
    migration = models.ForeignKey(Migration, on_delete=models.CASCADE, related_name='fields', null=True)
    field_type = models.CharField(
        max_length=4,
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



