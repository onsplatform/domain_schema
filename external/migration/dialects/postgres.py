from datetime import datetime

from ..commands import BaseCreateTableCommand, BaseRenameTableCommand, BaseAlterTableCommand


CONSTRAINTS = {
    "primary_key": 'PRIMARY KEY',
    "required": 'NOT NULL'
}


class PostgresCreateTableCommand(BaseCreateTableCommand):
    CONSTRAINTS = CONSTRAINTS

    def _build_column(self, name, _type, constraints):
        return  f'{name} {_type} {str.join(", ", constraints)}'.strip()

    def build_command(self):
        if not self.table_name:
            raise Exception('table name not set.')

        return f'CREATE TABLE "{self.table_name}"'

    def __repr__(self):
        return self.build_command()


class PostgresAlterTableCommand(BaseAlterTableCommand):
    CONSTRAINTS = CONSTRAINTS

    def _build_column(self, name, _type, constraints):
        return  f'ADD {name} {_type} {str.join(", ", constraints)}'.strip()

    def build_command(self):
        return f'ALTER TABLE "{self.table_name}"'


class PostgresRenameTableCommand(BaseRenameTableCommand):
    def build_command(self):
        return f'ALTER TABLE {self.table_name} RENAME TO {self.name}'


PostgresMigrationDialect = {
    'create_table': PostgresCreateTableCommand,
    'alter_table': PostgresAlterTableCommand,
    'rename_table': PostgresRenameTableCommand,
}
