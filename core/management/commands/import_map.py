from django.core.management.base import BaseCommand
from core.models import *
import yaml
import re
from django.db import transaction
import io


class MapLoader:
    def __init__(self, target_path, solution_name, app_name):
        self.target_path = target_path
        self.solution_name = solution_name
        self.app_name = app_name


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument(
            'target_path', type=str, help='Path containing yaml files to be imported.')
        parser.add_argument(
            'solution', type=str, help='Solution name.')
        parser.add_argument(
            'app', type=str, help='Application name.')
        parser.add_argument()

    @staticmethod
    def parse_arguments(**options):
        target_path = options.pop('target_path')
        solution_name = options.pop('solution', 'Sager')
        app_name = options.pop('app')

        return target_path, solution_name, app_name

    def handle(self, *args, **options):

        # Get solution
        solution = Solution.objects.get(name='Sager')

        app_name = 'SAGER_Cenario_Configuracao'

        if app_name:
            print(f"========================== {app_name} ==========================")
            # yaml_map = yaml.load(git_repos.get_map_content(repo_id), Loader=yaml.FullLoader)
            # import pdb; pdb.set_trace()
            with open('D:\ONS\SAGER\sager.cenario.configuracao.manter.fabrica\Mapa\SAGER_Cenario_Configuracao.map.yaml', 'r', encoding='utf-8') as f:
                stream = f.read()

            yaml_map = yaml.load(stream, Loader=yaml.FullLoader)

            map_app, _ = App.objects.get_or_create(name=app_name, solution=solution)

            # loop through dictionary to create EntityMap('agente', 'statusevento', etc)
            for map_key, map_value in yaml_map.items():
                with transaction.atomic():
                    map_name = map_key
                    map_entity = Entity.objects.get(name=map_value.get('model'))

                    # CREATE EntityMap needs: current app, model or entity and a name.
                    entity_map, _ = EntityMap.objects.get_or_create(name=map_name, app=map_app, entity=map_entity)

                    # CREATE fields: loop through fields in yaml file
                    self.create_fields(entity_map, map_entity, map_value['fields'])
                    # CREATE filters: loop through filters in yaml file
                    self.create_filters(entity_map, map_value.get('filters', {}))

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

                #import pdb; pdb.set_trace()
                # Get or Create a map_filter
                map_filter, created = MapFilter.objects.get_or_create(map=entity_map, name=filter_key, defaults={'expression': filter_value})

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

    @staticmethod
    def get_entity(entity_name: str):
        """ TODO: delete or refactor this! """
        # Get EntityMap or create it
        return Entity.objects.get(name=entity_name)