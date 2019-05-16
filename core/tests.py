from datetime import datetime

from django.test import TestCase

from core.utils.testing import *
from core.models import Solution, App, Migration, Entity, \
        Field, EntityMap, MappedField, FIELD_TYPES


class EntityModelTestCase(TestCase):
    def test_create_first_migration(self):
        # mock
        solution = Solution.objects.create(name='TestSolution')
        entity = Entity.objects.create(solution=solution, name='TestEntity', table='tb_test')
        field = Field.objects.create(entity=entity, name='test_field', field_type=FIELD_TYPES.CHAR)

        # act
        migration = entity.make_migration()

        # assert
        assert entity.migrations.count() == 1
        assert migration.first

    def test_create_next_migration(self):
        # mock
        solution = Solution.objects.create(name='TestSolution')
        entity = Entity.objects.create(solution=solution, name='TestEntity', table='tb_test')
        migration = Migration.objects.create(entity=entity) # pre exisiting migration
        field = Field.objects.create(entity=entity, name='test_field', field_type=FIELD_TYPES.CHAR)

        # act
        migration = entity.make_migration()

        # assert
        assert not migration.first


class MigrationModelTestCase(TestCase):
    def test_run_migration(self):
        # mock
        solution = Solution.objects.create(name='TestSolution')
        entity = Entity.objects.create(solution=solution, name='TestEntity', table='tb_test')
        migration = Migration.objects.create(entity=entity, first=True) # pre exisiting migration
        migration.fields.add(entity.fields.first())

        # act
        exectuted_migration = migration.run()

        # assert
        assert migration.date_executed <= datetime.now()


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
            'solution': Solution.objects.create(name='test_solution'),
        }

    def create_data(self):
        return {
            'name': 'test_entity',
            'table': 'test_table',
            'fields': [{
                'name': 'name',
                'field_type': 'char',
            }]
        }

    def update_data(self):
        return {
            'name': 'test_entity_upd',
            'table': 'test_table',
            'fields': [{
                'name': 'name',
                'field_type': 'char',
            }]
        }


class EntityMapTestCase(ModelAPITestCase):
    MODEL = EntityMap
    NESTED_MODELS = {
        'fields': MappedField,
    }
    __test__ = True

    def build_requirements(self):
        sln = Solution.objects.create(name='test_solution')
        app = App.objects.create(name='test_app', solution=sln)
        entity = Entity.objects.create(
            name='test_entity', solution=sln, table='tb_test_entity')

        return {
            'entity': entity,
            'app': app,
        }

    def create_data(self):
        field  = Field.objects.create(
            entity=self.requirements['entity'],
            name='test_field',
            field_type=FIELD_TYPES.INTEGER)

        return {
            'name': 'test_map',
            'fields': [{
                'field_id': field.id,
                'alias': 'test_alias',
            }]
        }

    def update_data(self):
        field  = Field.objects.create(
            entity=self.requirements['entity'],
            name='test_field',
            field_type=FIELD_TYPES.INTEGER)

        return {
            'name': 'test_map_upd',
            'fields': [{
                'field_id': field.id,
                'alias': 'test_alias',
            }]
        }
