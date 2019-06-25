from django.core.management.base import BaseCommand
from core.models import EntityMap, MappedField, MapFilter, MapFilterParameter, Entity, App
from core.utils import yaml_helper, azure_devops as tfs
import yaml


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
                print(yaml_map)
                # TODO: get or create sager solution
                # TODO: get or create App (need App Id for EntityMap)
                # TODO: get or create map



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

