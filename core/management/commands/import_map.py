from django.core.management.base import BaseCommand
from core.models import *
from core.utils import yaml_helper, azure_devops as tfs
import yaml
import re


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
                import pdb; pdb.set_trace()

                yaml_map = yaml.load(git_repos.get_map_content(repo_id), Loader=yaml.FullLoader)

                # CREATE App
                solution = Solution.objects.get(name='SAGER')
                map_app, _ = App.objects.get_or_create(name=app_name, solution=solution)

                # loop through dictionary to create EntityMap(Agente)
                for map_key, map_value in yaml_map.items():
                    map_name = map_key
                    map_entity = Entity.objects.get(name=map_value.get('model'))

                    # CREATE EntityMap needs: current app, model or entity and a name.
                    entity_map, _ = EntityMap.objects.get_or_create(name=map_name, app=map_app, entity=map_entity)

                    # CREATE fields: loop through fields in yaml file
                    fields = map_value.get('fields')
                    for field_key, field_value in fields.items():
                        current_field = Field.objects.get(name=field_value)
                        map_field, _ = MappedField.objects.get_or_create(entity_map=entity_map, field=current_field,
                                                                         alias=field_key)
                        print(field_key, field_value)

                    # CREATE filters: loop through filters in yaml file
                    filters = map_value.get('filters')
                    for filter_key, filter_value in filters.items():
                        map_filter, _ = MapFilter.objects.get_or_create(map=entity_map, name=field_key,
                                                                        expression=filter_value)
                        regex = r"([:\$]\w+)"
                        matches = re.finditer(regex, filter_value)

                        # for each match in the expression, create the appropriate parameter
                        for _, match_value in enumerate(matches, start=1):
                            array = match_value.group().startswith('$')
                            field_parameter = match_value.group()[1:]
                            MapFilterParameter.objects.get_or_create(filter=map_filter, name=field_parameter,
                                                                     is_array=array)
                        # CREATE filter parameters

                        print(filter_key, filter_value)

    @staticmethod
    def get_entity(entity_name: str):
        """ TODO: delete or refactor this! """
        # Get EntityMap or create it
        return Entity.objects.get(name=entity_name)

"""


        # if there are yaml files at path
        if yaml_file:
            with open(yaml_file, 'r', encoding='utf-8') as stream:
                # load Yaml file stream
                yaml_dict = yaml.load(stream, Loader=yaml.FullLoader)

                # run through the dictionary to populate entities
                for key, value in yaml_dict.items():
                    entity = Entity.objects.get(value.get('model'))
                    fields = value.get('fields')
                    filters = value.get('filters')

                    entity_map, _ = EntityMap.objects.all().get_or_create(name=key, entity=entity)
"""

