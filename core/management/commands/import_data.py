from django.core.management.base import BaseCommand
from os import walk, path
import yaml
import io
from glob import glob
from typing import List

class Command(BaseCommand):
    def handle(self, **options):
        # open folder and load yaml files list within it.
        yamlList = self.listYamlFiles('./domain_schema/core/management/commands/')

        # if there are yaml files at path
        if yamlList:
            # open each file, and load it´s contents. FullLoader is safe.
            for file in yamlList:
                with open(file, 'r', enconding='utf-8') as stream:
                    yamlFile = yaml.load(stream,Loader=yaml.FullLoader)
                    # ... record entity

        
        # ler yaml
        # colocar num dict
        # ex:
        # data = [
        # {
        #  solution=1,
        #  name="usina",
        # },
        # {
        #  solution=1,
        #  name="usina",
        # },
        # ]

        #entiies = [Entity(**d) for d in data]

        #print('do it here...')
        import pdb; pdb.set_trace()  
        x = 1
        pass
    
    def listFiles(self):
        next(walk('./domain_schema'))
        return 'x'

    def listYamlFiles(self, filepath) -> List:
        """ Returns a list of YAML files in a given path.
        """       
        # check if path exists
        if path.exists(filepath):
            yamlFiles = glob(filepath + '*.yaml')
            return yamlFiles