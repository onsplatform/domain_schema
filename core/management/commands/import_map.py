from django.core.management.base import BaseCommand
from core.models import *
from core.utils import azure_devops as tfs
import yaml
import re
from django.db import transaction


class Command(BaseCommand):
    def handle(self, *args, **options):

        # get a new project repository instance
        git_repos = tfs.AzureDevops('weo6dxvr6l6e557q3feya7ijqfxxxfmfyhnat4fnqxawouoydvdq', 'sager')

        repository_id_list = git_repos.list_repo_id()

        # CREATE App
        solution = Solution.objects.get(name='SAGER')

        for repo_id in repository_id_list:
            # get App name from 'plataforma.json' in the root of the git repository.)
            app_name = git_repos.get_app_name_from_yaml(repo_id)
            if app_name:
                print(f"========================== {app_name} ==========================")

                yaml_map = yaml.load(git_repos.get_map_content(repo_id), Loader=yaml.FullLoader)

                with transaction.atomic():
                    map_app, _ = App.objects.get_or_create(name=app_name, solution=solution)

                    # loop through dictionary to create EntityMap('agente', 'statusevento', etc)
                    for map_key, map_value in yaml_map.items():
                        map_name = map_key
                        map_entity = Entity.objects.get(name=map_value.get('model'))

                        # CREATE EntityMap needs: current app, model or entity and a name.
                        entity_map, _ = EntityMap.objects.get_or_create(name=map_name, app=map_app, entity=map_entity)

                        # CREATE fields: loop through fields in yaml file
                        self.create_fields(entity_map, map_entity, map_value['fields'])
                        # CREATE filters: loop through filters in yaml file
                        self.create_filters(entity_map, map_value.get('filters', {}))

    def create_fields(self, entity_map, map_entity, map_value):

        for field_key, field_value in map_value.items():
            print(f"Entidate: {entity_map.name} == Field Key: {field_key}, Field Value: {field_value.get('column')}")
            current_field = Field.objects.filter(name=field_value.get('column'), entity=map_entity).first()

            if not current_field:
                print(f"Field {field_key} not found in {entity_map.name}. Ignoring...")
                continue

            map_field, _ = MappedField.objects.get_or_create(entity_map=entity_map, field=current_field,
                                                                 alias=field_key)

    def create_filters(self, entity_map, map_value):

        for filter_key, filter_value in map_value.items():
            if filter_value:
                # Get or Create a map_filter
                map_filter, _ = MapFilter.objects.get_or_create(map=entity_map, name=filter_key,
                                                                expression=filter_value)
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
