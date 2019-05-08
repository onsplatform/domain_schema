from django.test import TestCase


from core.utils.testing import *
from core.models import Solution, App, Migration, Entity, \
        Field, EntityMap, MappedField, FIELD_TYPES


class MigrationTestCase(TestCase):
    def test_create_table(self):
        # mock
        solution = Solution.objects.create(name='TestSolution')
        entity = Entity.objects.create(solution=solution, name='TestEntity', table='tb_test')
        field = Field.objects.create(entity=entity, field_type=FIELD_TYPES.CHAR, name='test_field')

        # act
        migration = entity.make_migration()
        # migrate_command = migration.create_table()

        # assert
        assert migration.first == True
        # assert migrate_command.__class__.__name__.endswith('CreateTableCommand')
        # assert migrate_command.table_name == 'tb_test'
        # assert field.name in migrate_command.columns

    def test_alter_table(self):
        # mock
        solution = Solution.objects.create(name='TestSolution')
        entity = Entity.objects.create(solution=solution, name='TestEntity', table='tb_test')
        migration = Migration.objects.create(entity=entity) # pre exisiting migration

        # adding new field to entity.
        field = Field(name='test_field', field_type=FIELD_TYPES.CHAR)
        entity.fields.add(field, bulk=False)

        # act
        migration = entity.make_migration()
        # create_table_command = migration.alter_table()

        # assert
        assert not migration.first
        # assert create_table_command.__class__.__name__.endswith('AlterTableCommand')
        # assert create_table_command.table_name == 'tb_test'
        # assert 'test_field' in create_table_command.add_columns


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

