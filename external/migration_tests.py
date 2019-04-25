from .migration import SQLiteMigrationDialect, DatabaseMigration


def test_migration():
        # mock
        dialect = SQLiteMigrationDialect()
        migraton = DatabaseMigration(dialect)

        # act
        migration = migraton.create_table('my_table') \
            .with_column('id', 'Int', primary_key=True) \
            .with_column('name', 'VarChar', required=True)

        # assert
        assert migration.build() == \
            'CREATE TABLE my_table (id Int PRIMARY KEY, name VarChar NOT NULL);'
