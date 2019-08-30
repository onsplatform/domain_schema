from django.core.management.base import BaseCommand
from core.models import *
from core.utils import azure_devops as tfs
import yaml
import re
from django.db import transaction
import io


class Command(BaseCommand):
    def handle(self, *args, **options):

        # get a new project repository instance
        git_repos = tfs.AzureDevops('weo6dxvr6l6e557q3feya7ijqfxxxfmfyhnat4fnqxawouoydvdq', 'sager')

        repository_id_list = git_repos.list_repo_id()

        # CREATE App
        solution = Solution.objects.get(name='SAGER')

        # for repo_id in repository_id_list:
        # get App name from 'plataforma.json' in the root of the git repository.)
        # app_name = git_repos.get_app_name_from_yaml(repo_id)
        app_name = 'SAGER_Evento'
        if app_name:
            print(f"========================== {app_name} ==========================")
            # yaml_map = yaml.load(git_repos.get_map_content(repo_id), Loader=yaml.FullLoader)
            # import pdb; pdb.set_trace()
            with open('D:\platform\domain_schema\core\management\commands\SAGER_Cenario.map.yaml', 'r', encoding='utf-8') as f:
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

