from datetime import datetime

from ..commands import BaseCreateTableCommand, BaseRenameTableCommand, BaseAlterTableCommand


CONSTRAINTS = {
    "primary_key": 'PRIMARY KEY',
    "required": 'NOT NULL'
}


class SQLiteCreateTableCommand(BaseCreateTableCommand):
    CONSTRAINTS = CONSTRAINTS

    def _build_column(self, name, _type, constraints):
        return  f'{name} {_type} {str.join(", ", constraints)}'.strip()

    def build_command(self):
        return f'CREATE TABLE {self.table_name}'


class SQLiteAlterTableCommand(BaseAlterTableCommand):
    CONSTRAINTS = CONSTRAINTS

    def _build_column(self, name, _type, constraints):
        return  f'ADD {name} {_type} {str.join(", ", constraints)}'.strip()

    def build_command(self):
        return f'ALTER TABLE {self.table_name}'


class SQLiteRenameTableCommand(BaseRenameTableCommand):
    def build_command(self):
        return f'ALTER TABLE {self.table_name} RENAME TO {self.name}'


SQLiteMigrationDialect = {
    'create_table': SQLiteCreateTableCommand,
    'alter_table': SQLiteAlterTableCommand,
    'rename_table': SQLiteRenameTableCommand,
}
