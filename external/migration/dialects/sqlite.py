from datetime import datetime

from ..commands import BaseCreateTableCommand, BaseRenameTableCommand


CONSTRAINTS = {
    "primary_key": 'PRIMARY KEY',
    "required": 'NOT NULL'
}


class SQLiteCreateTableCommand(BaseCreateTableCommand):
    CONSTRAINTS = CONSTRAINTS

    def _build_column(self, name, _type, constraints):
        return  f'{name} {_type} {str.join(", ", constraints)}'

    def build_command(self):
        return f'CREATE TABLE {self.table_name}'


class SQLiteAlterTableCommand(BaseCreateTableCommand):
    CONSTRAINTS = CONSTRAINTS

    def _build_column(self, name, _type, constraints):
        return  f'{name} {_type} {str.join(", ", constraints)}'

    def build_command(self):
        return f'ALTER TABLE {self.table_name}'


class SQLiteRenameTableCommand(BaseRenameTableCommand):
    def build_command(self):
        return f'ALTER TABLE {self.table_name} RENAME TO {self.name}'


class SQLiteMigrationDialect:
    def create_table(self, table_name):
        return SQLiteCreateTableCommand(table_name)

    def alter_table(self, table_name):
        return SQLiteAlterTableCommand(table_name)

    def rename_table(self, table_name):
        return SQLiteRenameTableCommand(table_name)
