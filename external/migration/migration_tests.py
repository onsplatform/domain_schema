from . import DatabaseMigration
from .dialects.sqlite import SQLiteMigrationDialect as dialect


migraton = DatabaseMigration(dialect)


def test_create_table():
    # act
    command = migraton.create_table('my_table') \
        .with_column('id', 'Int', primary_key=True) \
        .with_column('name', 'VarChar', required=True)

    # assert
    assert command.build() == \
        'CREATE TABLE my_table (id Int PRIMARY KEY, name VarChar NOT NULL);'


def test_alter_table():
    # act
    command = migraton.alter_table('my_table') \
        .add_column('new_col', 'Int',) \

    # assert
    assert command.build() == \
        'ALTER TABLE my_table ADD new_col Int;'


def test_rename_table_command():
    # act
    command = migraton.rename_table('my_table').to('my_new_table')

    # assert
    assert command.build() == \
        'ALTER TABLE my_table RENAME TO my_new_table'


