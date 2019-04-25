from datetime import datetime

from core.models import Entity


class DatabaseMigration:
    def __init__(self, dialect):
        self.dialect = dialect

    def create_table(self, table_name):
        return self.dialect.create_table(table_name)



class BaseCreateTableCommand:
    SEPARATOR = ', '
    GROUP_START = '('
    GROUP_END = ')'
    DELIMITER = ';'

    def __init__(self, table_name):
        self.table_name = table_name
        self.columns = []

    def with_column(self, name, _type, required=False, primary_key=False, **kwargs):
        self.columns.append((name, _type, required, primary_key, kwargs))
        return self

    def build(self):
        columns = str.join(
            self.SEPARATOR,
            [self.build_column(c) for c in self.columns]
        )
        return f'{self.build_table()} {self.GROUP_START}{columns}{self.GROUP_END}{self.DELIMITER}'


class SQLiteCreateTableCommand(BaseCreateTableCommand):
    def build_table(self):
        return f'CREATE TABLE {self.table_name}'

    def build_column(self, column,):
        name, _type, required, pk, _ = column
        cmd =  f'{name} {_type}'

        if pk:
            cmd += ' PRIMARY KEY'

        if required:
            cmd += ' NOT NULL'

        return cmd


class SQLiteMigrationDialect:
    def create_table(self, table_name):
        return SQLiteCreateTableCommand(table_name)



def migrate(entity):
    if not entity.migration:
        return

    assert 1 == 2

