import yaml
from django.core.management.base import BaseCommand

from core.models import Entity, Solution, Field
from core.utils import yaml_helper


class Command(BaseCommand):
    def handle(self, **options):
        """
        Dictionary sample the code above will import.
            {'e_ageoper': 
                {
                    'id_age': ['string'], 
                    'ido_ons': ['string'], 
                    'nom_curto': ['string'], 
                    'dat_entrada': ['datetime'], 
                    'dat_desativacao': ['datetime'], 
                    'nom_longo': ['string']
                }
            }
        """
        # open folder and list all yaml files within it.
        # TODO: refactor this to receive directory as a parameter
        yaml_files = yaml_helper.list_files('./core/management/commands/')

        # make sure the solution is created or exists before creating new Entities
        sln = self.create_solution('SAGER')

        # if there are yaml files at path
        if yaml_files:
            # for each file in folder...
            for file in yaml_files:
                try:
                    entity_name: str = ''
                    fields = {}
                    my_entity = None

                    # Open file, read it, populate variables, close file.
                    # Perhaps we should extract a method here...
                    with open(file, 'r', encoding='utf-8') as stream:
                        yaml_dict = yaml.load(stream, Loader=yaml.FullLoader)

                        for data in yaml_dict.items():
                            my_entity = self.create_entity(name=data[0], solution=sln)
                            fields = data[1]

                    # Create Entity and link Fields to it.
                    my_entity.name = entity_name

                    # We have to review this loop
                    for k, v in fields.items():
                        my_field = Field()
                        my_field.name = k
                        my_field.field_type = v[0]
                        my_field.entity = my_entity
                        my_field.save()

                except OSError:
                    return "Program was not able to open file at given destination"

    @staticmethod
    def create_solution(solution_name: str):
        """
        Creates a solution or returns a Solution object if it already exists.
        """
        # Delete all solution objects and recreate them
        Solution.objects.all().delete()

        if not Solution.objects.filter(name=solution_name).exists():
            solution = Solution.objects.create(name=solution_name)
            return solution

        solution = Solution.objects.get(name=solution_name)

        return solution

    @staticmethod
    def create_entity(**kwargs):
        """
        Creates an Entity or returns an entity being called.
        """
        if not Entity.objects.filter(**kwargs).exists():
            current_entity = Entity.objects.create(**kwargs)
            return current_entity

        current_entity = Entity.objects.get(**kwargs)
        return current_entity
