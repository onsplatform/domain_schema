from . import DatabaseMigration
from .dialects.postgres import PostgresMigrationDialect as dialect


migraton = DatabaseMigration(dialect)


def test_create_table_with_primary_key():
    # act
    command = migraton.create_table('my_table') \
        .with_column('id', 'Int', primary_key=True) \

    # assert
    assert command.build() == \
        'CREATE TABLE "my_table" (id Int PRIMARY KEY);'


def test_create_table_with_required_field():
    # act
    command = migraton.create_table('my_table') \
        .with_column('col', 'Int', required=True) \

    # assert
    assert command.build() == \
        'CREATE TABLE "my_table" (col Int NOT NULL);'


def test_create_table_with_foreign_key():
    # act
    command = migraton.create_table('my_table') \
        .with_column('fk', 'Int', references=('tb_parent','id'))\

    # assert
    assert command.build() == \
        'CREATE TABLE "my_table" (fk Int REFERENCES tb_parent(id));'

def test_create_table_with_default_value_column():
    # act
    command = migraton.create_table('my_table') \
        .with_column('col', 'Int', default=0)\

    # assert
    assert command.build() == \
        'CREATE TABLE "my_table" (col Int DEFAULT 0);'


def test_alter_table():
    # act
    command = migraton.alter_table('my_table') \
        .add_column('new_col', 'Int',) \

    # assert
    assert command.build() == \
        'ALTER TABLE "my_table" ADD new_col Int;'


def test_rename_table_command():
    # act
    command = migraton.rename_table('my_table').to('my_new_table')

    # assert
    assert command.build() == \
        'ALTER TABLE my_table RENAME TO my_new_table'
