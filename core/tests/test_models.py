import pytest

from django.test import TestCase

from core.models import Solution, App, Migration, Entity, \
        Field, EntityMap, MappedField, FIELD_TYPES
from core.utils import postgres as pg
from core.tasks import apply_model_migration


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
    DATA_SCHEMA = {
        'id': {
            'column_default': 'uuid_generate_v4()',
            'is_nullable': 'NO',
            'data_type': 'uuid'
        },
        'date_created': {
            'column_default': 'now()',
            'is_nullable': 'NO',
            'data_type': 'timestamp without time zone'
        },
    }

    HISTORY_SCHEMA = {
        'id': {
            'column_default': None,
            'is_nullable': 'NO',
            'data_type': 'uuid',
        },
        'version_id': {
            'column_default': 'uuid_generate_v4()',
            'is_nullable': 'NO',
            'data_type': 'uuid',
        },
        'date_created': {
            'column_default': None,
            'is_nullable': 'NO',
            'data_type': 'timestamp without time zone',
        },
    }

    def assert_table_schema_equals_to(self, table_name, schema):
        table_cols = pg.table_columns('entities', table_name)

        for col_name, col_schema in schema.items():
            assert col_name in table_cols, f'expected column {col_name} was not found in the schema.'

            for constraint_name, constraint_value in col_schema.items():
                existing_val = table_cols[col_name][constraint_name]
                assert constraint_value == existing_val,\
                    f'{constraint_name} is expected to be {constraint_value} but was {existing_val}'

    def test_entity_migraiton_create_data_schema(self):
        sln = Solution.objects.create(name='test_solution')
        entity = Entity.objects.create(solution=sln, name='test_entity', table='tb_test_entity')

        migration = entity.make_migration()
        apply_model_migration.run(migration.id)

        # assert both entity and entity history tables were created.
        assert pg.table_exists('entities', 'tb_test_entity')
        assert pg.table_exists('entities', 'tb_test_entity_history')

        # assert data schemas were created correctly.
        self.assert_table_schema_equals_to('tb_test_entity', self.DATA_SCHEMA)
        self.assert_table_schema_equals_to('tb_test_entity_history', self.HISTORY_SCHEMA)

        # assert migration was marked as executed.
        migration.refresh_from_db()
        assert migration.date_executed is not None


class EntityMapModelTest(TestCase):
    def test_create_map_add_id_field_by_default(self):
        sln = Solution.objects.create(name='test_solution')
        entity = Entity.objects.create(solution=sln, name='test_entity')
        app = App.objects.create(solution=sln, name='test_app')

        # act
        entity_map = EntityMap.objects.create(app=app, entity=entity, name='test_map')

        # assert
        assert entity_map.fields.filter(field__name='id').count() == 1
