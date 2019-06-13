from django.core.management.base import BaseCommand
from os import walk, path
import yaml, io
from glob import glob
from typing import List

from core.models import Entity, Solution, Field

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
        yamlFiles = self.listYamlFiles('./core/management/commands/')
        
        # make sure the solution is created or exists before creating new Entities
        sln = self.createSolution('SAGER')

        # if there are yaml files at path
        if yamlFiles:
            # for each file in folder...
            for file in yamlFiles:
                
                try:
                    entityName = ''
                    fields = {}
                    myEntity = None
                                      
                    # Open file, read it, populate variables, close file.
                    # Perhaps we should extract a method here...
                    with open(file, 'r', encoding='utf-8') as stream:
                        yamlDict = yaml.load(stream,Loader=yaml.FullLoader)

                        for data in yamlDict.items():
                            myEntity = self.createEntity(name=data[0], solution=sln)
                            fields = data[1]

                    # Create Entity and link Fields to it.
                    myEntity.name = entityName

                    # We have to review this loop
                    for k,v in fields.items():
                        myField = Field()
                        myField.name = k
                        myField.field_type = v[0]
                        myField.entity = myEntity
                        #myEntity.fields.add(myField)
                        myField.save()

                except OSError:
                    return "Program was not able to open file at given destination"

        
    def createSolution(self, solutionName):
        """
        Creates a solution or returns a Solution object if it already exists.
        """
        solution = None

        # Delete all solution objects and recreate them
        Solution.objects.all().delete()

        if not Solution.objects.filter(name=solutionName).exists():
            solution = Solution.objects.create(name=solutionName)
            return solution
        
        solution = Solution.objects.get(name=solutionName)

        return solution


    def createEntity(self, **kwargs):
        """
        Creates an Entity or returns an entity being called.
        """
        currentEntity = None
        if not Entity.objects.filter(**kwargs).exists():
            currentEntity = Entity.objects.create(**kwargs)
            return currentEntity
        
        currentEntity = Entity.objects.get(**kwargs)
        return currentEntity  

    def listYamlFiles(self, filepath) -> List:
        """ Returns a list of YAML files in a given path.
        """       
        # check if path exists
        if path.exists(filepath):
            yamlFiles = glob(filepath + '*.yaml')
            return yamlFiles