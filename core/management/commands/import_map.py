from django.core.management.base import BaseCommand
from core.models import EntityMap, MappedField, MapFilter, MapFilterParameter, Entity
from core.utils import yaml_helper, azure_devops as tfs
import yaml


class Command(BaseCommand):
    def handle(self, *args, **options):

        # get a new project repository instance
        git_repos = tfs.AzureDevops('weo6dxvr6l6e557q3feya7ijqfxxxfmfyhnat4fnqxawouoydvdq', 'sager')

        ids = git_repos.list_repo_id()

        for item in ids:
            import pdb; pdb.set_trace()
            if git_repos.get_app_name(item) is not None:
                print(git_repos.get_app_name(item))

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

