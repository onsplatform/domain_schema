from datetime import datetime

from django.test import TestCase
from rest_framework.test import APITestCase, APIClient
from django.db import connection, transaction

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



@pytest.mark.usefixtures("celery_app")
class MigrationModelTestCase(TestCase):
    def test_run_migration(self):
        # mock
        solution = Solution.objects.create(name='TestSolution')
        entity = Entity.objects.create(solution=solution, name='TestEntity', table='tb_test')
        migration = Migration.objects.create(entity=entity, first=True) # pre exisiting migration
        migration.fields.add(entity.fields.first())

        # act
        migration.run()

        # assert
        migration.refresh_from_db()
        assert migration.date_executed is not None



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


def table_exists(table_schema, table_name):
    with connection.cursor() as cursor:
        query = f"""
            SELECT COUNT(*)
            FROM information_schema.tables
            WHERE table_schema = '{table_schema}' AND table_name = '{table_name}'
        """
        cursor.execute(query)
        ret = cursor.fetchone()
        return ret[0] > 0

def table_columns(table_schema, table_name) :
        with connection.cursor() as cursor:
            cursor.execute(f"""
                SELECT column_name, column_default, is_nullable, data_type
                FROM "information_schema"."columns"
                WHERE table_schema='{table_schema}' AND table_name = '{table_name}'
            """)

            columns = [col[0] for col in cursor.description]
            return {row[0]: dict(zip(columns[1:], row[1:])) for row in cursor.fetchall()}

class PostgresVersioningSchemaTestCase(APITestCase):
    def test_create_entity_creates_data_schema(self):
        # mock
        sln = Solution.objects.create(name='test_solution')
        data = {
            "name": "Entity",
            "solution_id": sln.id,
            "table": "tb_entity",
        }

        # act
        response = self.client.post('/api/entity/', data, format='json')

        # assert
        # assert table was created
        assert table_exists('entities', 'tb_entity_history')

        # assert table schema is correct
        columns = table_columns('entities', 'tb_entity_history')

        # version_id primary key column
        version_id_column = columns['version_id']
        assert version_id_column['column_default'] == 'entities.uuid_generate_v4()'
        assert version_id_column['is_nullable'] == 'NO'
        assert version_id_column['data_type'] == 'uuid'
        # TODO: check is primary key
        # TODO: check the rest of the schema
        # TODO: move this test to another location.


    def test_updating_data_entity_creates_history_version(self):
        # mock
        sln = Solution.objects.create(name='test_solution')
        entity = Entity.objects.create(
            name='test_entity', solution=sln, table='tb_test_entity')

        entity



