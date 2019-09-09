import os

import yaml
from django.core.management.base import BaseCommand
from django.db import transaction

from core.models import Entity, Solution, Field, FIELD_TYPES
from core.tasks import apply_model_migration
from core.utils import yaml_helper


# todo: Check if Solutions are taking only the name. Sager was created as "Solution=Sager" instead of just "Sager"

class EntityLoader:
    MAP_TYPES = {
        "string": FIELD_TYPES.VARCHAR,
        "text": FIELD_TYPES.TEXT,
        "integer": FIELD_TYPES.INTEGER,
        "date": FIELD_TYPES.DATE,
        "datetime": FIELD_TYPES.DATE,
        "double": FIELD_TYPES.DECIMAL,
        "boolean": FIELD_TYPES.BOOLEAN,
    }

    def __init__(self, target_path, solution_name, delete_existing_solution=False):
        self.target_path = target_path
        self.solution_name = solution_name
        self.delete_existing_solution = delete_existing_solution

    def create_fields(self, entity, fields):
        for k, v in fields.items():
            field_type = self.MAP_TYPES[v[0]]
            field = Field(entity=entity, name=k, field_type=field_type)
            if field_type == self.MAP_TYPES['string']:
                field.precision = 200
            yield field

    def create_entity(self, source_file, solution):
        with open(source_file, 'r', encoding='utf-8') as stream:
            yaml_dict = yaml.load(stream, Loader=yaml.FullLoader)

        for name, fields in yaml_dict.items():
            # create entity metadata.
            entity = Entity.objects.create(name=name, solution=solution)
            entity_fields = self.create_fields(entity, fields)
            Field.objects.bulk_create(entity_fields)

            # create database structure.
            migration = entity.make_migration()
            apply_model_migration.run(migration.id)

            return entity

    def run(self):
        with transaction.atomic():
            if self.delete_existing_solution:
                Solution.objects.all().delete()

            solution, _ = Solution.objects.get_or_create(name=self.solution_name)

            return [
                self.create_entity(f, solution)
                for f in yaml_helper.walk_files(self.target_path)]


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            'target_path', type=str, help='Path containing yaml files to be imported.')
        parser.add_argument(
            'solution', type=str, help='Solution name.')
        parser.add_argument(
            '-c', '--clear_before_import', action='store_true', help='Delete existing solution before importing.')

    def parse_arguments(self, **options):
        target_path = options.pop('target_path')
        clear_before_import = options.pop('clear_before_import')
        solution_name = options.pop('solution', 'SAGER')
        return target_path, clear_before_import, solution_name

    def handle(self, **options):
        target_path, clear_before_import, solution_name = self.parse_arguments(**options)

        if not os.path.exists(target_path):
            return '** target directory does not exist.'

        loader = EntityLoader(target_path, solution_name, clear_before_import)
        entities = loader.run()
        print(f"** {len(list(entities))} entities installed.")


