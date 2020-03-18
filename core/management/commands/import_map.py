import os
import re
from django.core.management.base import BaseCommand
from core.models import *
import yaml
from django.db import transaction


class MapLoader:
    def __init__(self, target_path: str = None, solution_name: str = None, app_name: str = None):
        self.target_path = target_path
        self.solution_name = solution_name
        self.app_name = app_name

    @staticmethod
    def create_fields(entity_map, map_entity, map_value):
        for field_key, field_value in map_value.items():
            print(f"Entidade: {entity_map.name} == Field Key: {field_key}, Field Value: {field_value.get('column')}")
            current_field = Field.objects.filter(name=field_value.get('column'), entity=map_entity).first()

            if not current_field:
                print(f":: ERROR :: Field {field_key} not found in {entity_map.name}. ==> Ignoring...")
                continue
            map_field, _ = MappedField.objects.get_or_create(entity_map=entity_map, field=current_field,
                                                             defaults={'alias': field_key})

    def create_filters(self, entity_map, map_value):
        for filter_key, filter_value in map_value.items():
            if filter_value:
                # Get or Create a map_filter
                map_filter, created = MapFilter.objects.get_or_create(map=entity_map, name=filter_key,
                                                                      defaults={'expression': filter_value})

                # Proceed to obtain and persist the parameters.
                self.create_filter_parameters(filter_value, map_filter)

    @staticmethod
    def create_filter_parameters(filter_value, map_filter):
        regex = r"([:\$]\w+)"
        matches = re.finditer(regex, filter_value)

        # for each match in the expression, create the appropriate parameter
        for _, match_value in enumerate(matches, start=1):
            array = match_value.group().startswith('$')
            field_parameter = match_value.group()[1:]
            MapFilterParameter.objects.get_or_create(filter=map_filter, name=field_parameter, is_array=array)

    def create_maps(self, yaml_dict, app_name, app_version):
        with transaction.atomic():
            app = App.objects.get(name=app_name)
            app_version = AppVersion.objects.get(app=app, version=app_version)

            for map_name, map_value in yaml_dict.items():
                entity = Entity.objects.get(name=map_value.get('model'))
                EntityMap.objects.get(name=map_name, app_version=app_version, entity=entity).delete()
                entity_map = EntityMap.objects.create(name=map_name,
                                                      app_version=app_version,
                                                      entity=entity)
                self.create_fields(entity_map, entity, map_value['fields'])
                self.create_filters(entity_map, map_value.get('filters', {}))

    def run(self):
        with transaction.atomic():
            print(f"========================== {self.app_name} ==========================")
            with open(self.target_path, 'r', encoding='utf-8') as f:
                stream = f.read()
            # Get solution id
            solution = Solution.objects.get(name=self.solution_name)

            yaml_map = yaml.load(stream, Loader=yaml.FullLoader)
            self.create_maps(yaml_map, solution, self.app_name, '1.0')


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('target_path', type=str, help='Complete path and yaml file name to be imported.')
        parser.add_argument('solution', type=str, help='Solution name.')
        parser.add_argument('app', type=str, help='Application name.')

    @staticmethod
    def parse_arguments(**options):
        target_path = options.pop('target_path')
        solution_name = options.pop('solution')
        app_name = options.pop('app')

        return target_path, solution_name, app_name

    def handle(self, *args, **options):
        target_path, solution_name, app_name = self.parse_arguments(**options)

        if not os.path.exists(target_path):
            return '** target directory or file does not exist.'

        loader = MapLoader(target_path, solution_name, app_name)
        loader.run()
