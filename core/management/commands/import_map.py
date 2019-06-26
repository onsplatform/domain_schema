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

        for repo_id in repository_id_list:
            # get App name from 'plataforma.json' in the root of the git repository.
            app_name = git_repos.get_app_name(repo_id)
            if app_name is not None:
                print(f"========================== {app_name} ==========================")
                yaml_map = yaml.load(git_repos.get_map_content(repo_id), Loader=yaml.FullLoader)
                # CREATE App
                solution = Solution.objects.get(name='SAGER')

                with transaction.atomic():
                    map_app, _ = App.objects.get_or_create(name=app_name, solution=solution)

                    # loop through dictionary to create EntityMap(Agente)
                    for map_key, map_value in yaml_map.items():
                        map_name = map_key
                        map_entity = Entity.objects.get(name=map_value.get('model'))

                        # CREATE EntityMap needs: current app, model or entity and a name.
                        entity_map, _ = EntityMap.objects.get_or_create(name=map_name, app=map_app, entity=map_entity)

                        # CREATE fields: loop through fields in yaml file
                        self.create_fields(entity_map, map_entity, map_value)

    def create_fields(self, entity_map, map_entity, map_value):
        fields = map_value.get('fields')
        for field_key, field_value in fields.items():
            # import pdb; pdb.set_trace()
            current_field, created = Field.objects.get_or_create(name=field_value.get('column'), entity=map_entity)

            if not created:
                print(f"Field Key: {field_key}, Field Value: {field_value.get('column')}")
                map_field, _ = MappedField.objects.get_or_create(entity_map=entity_map, field=current_field,
                                                                 alias=field_key)

                # CREATE filters: loop through filters in yaml file
                self.create_filters(entity_map, field_key, map_value)

    def create_filters(self, entity_map, field_key, map_value):
        filters = map_value.get('filters')
        if filters is not None:
            for filter_key, filter_value in filters.items():
                if filter_value is not None:
                    map_filter, _ = MapFilter.objects.get_or_create(map=entity_map, name=field_key,
                                                                    expression=filter_value)
                    # CREATE filter parameters
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
