import pytest

from core.utils.testing import *

from core.models import Solution, App, Entity, \
        Field, EntityMap, MappedField, FIELD_TYPES


class SolutionTestCase(ModelAPITestCase):
    MODEL = Solution
    __test__ = True

    def update_data(self):
        return {
            'name': 'test_solution_upd'
        }

    def create_data(self):
        return {
            'name': 'test_solution'
        }


class AppTestCase(ModelAPITestCase):
    MODEL = App
    __test__ = True

    def build_requirements(self):
        return {
            'solution': Solution.objects.create(name='test_solution')
        }

    def create_data(self):
        return {
            'name': 'test_app'
        }

    def update_data(self):
        return {
            'name': 'test_app_upd'
        }


class EntityTestCase(ModelAPITestCase):
    MODEL = Entity
    NESTED_MODELS = {'fields': Field}
    __test__ = True

    def build_requirements(self):
        return {
            'solution': Solution.objects.create(name='test_solution')
        }

    def create_data(self):
        return {
            'name': 'test_entity',
            'fields': [{
                'name': 'name',
                'field_type': 'char',
            }]
        }

    def update_data(self):
        return {
            'name': 'test_entity_upd',
            'fields': [{
                'name': 'name',
                'field_type': 'char',
            }]
        }

class EntityMapTestCase(ModelAPITestCase):
    MODEL = EntityMap
    NESTED_MODELS = {'fields': MappedField}
    __test__ = True

    def build_requirements(self):
        sln = Solution.objects.create(name='test_solution')
        app = App.objects.create(name='test_app', solution=sln)
        entity = Entity.objects.create(name='test_entity', solution=sln, table='tb_test_entity')

        return {
            'solution': sln,
            'app': app,
            'entity': entity,
        }

    def create_data(self):
        sln = Solution.objects.create(name='test_solution')
        entity = Entity.objects.create(name='test_entity', solution=sln, table='tb_test_entity')
        field  = Field.objects.create(entity=entity, name='test_field', field_type=FIELD_TYPES.INTEGER)

        return {
            'name': 'test_map',
            'fields': [{
                'field_id': field.id,
                'alias': 'test_alias',
            }]
        }

    def update_data(self):
        sln = Solution.objects.create(name='test_solution')
        entity = Entity.objects.create(name='test_entity', solution=sln, table='tb_test_entity')
        field  = Field.objects.create(entity=entity, name='test_field', field_type=FIELD_TYPES.INTEGER)

        return {
            'name': 'test_map_upd',
            'fields': [{
                'field_id': field.id,
                'alias': 'test_alias',
            }]
        }

