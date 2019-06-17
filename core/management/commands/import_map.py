from django.core.management.base import BaseCommand
from core.models import EntityMap, MappedField, MapFilter, MapFilterParameter, Entity
from core.utils import yaml_helper
import yaml
import typing


class Mapping(BaseCommand):
    def handle(self, *args, **options):


        # open folder and list all yaml files within it.
        yaml_file = yaml_helper.list_files('d:/platform/domain_schema/core/management/commands/map.yaml')

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



        return None

    @staticmethod
    def get_entity(entity_name: str):
        """ TODO: delete or refactor this! """
        # Get EntityMap or create it
        return Entity.objects.get(name=entity_name)
