from datetime import datetime

from ..commands import BaseCreateTableCommand, BaseRenameTableCommand, BaseAlterTableCommand


CONSTRAINTS = {
    "primary_key": 'PRIMARY KEY',
    "required": 'NOT NULL',
    "references": 'REFERENCES {schema}.{table}({column})',
    "default": 'DEFAULT {default}',
    "precision": "({precision})"
}


class PostgresCreateTableCommand(BaseCreateTableCommand):
    CONSTRAINTS = CONSTRAINTS

    def _build_column(self, column):
        refs = None
        default = None
        precision = None

        if column.references:
            table, col = column.references
            refs = self.CONSTRAINTS["references"].format(schema=self.schema, table=table, column=col)

        if column.default is not None:
            default = self.CONSTRAINTS['default'].format(default=column.default)

        if column.precision:
            precision = self.CONSTRAINTS['precision'].format(precision=column.precision)

        fields = [column.name, str(column.field_type), precision, refs, default,
                  str.join(",", column.constraints)]

        return str.join(' ', filter(None, fields))

    def build_command(self):
        if not self.table_name:
            raise Exception('table name not set.')

        return f'CREATE TABLE {self.schema}."{self.table_name}"'


class PostgresAlterTableCommand(BaseAlterTableCommand):
    CONSTRAINTS = CONSTRAINTS

    def _build_column(self, name, _type, constraints):
        return  f'ADD {name} {_type} {str.join(", ", constraints)}'.strip()

    def build_command(self):
        return f'ALTER TABLE {self.schema}."{self.table_name}"'


class PostgresRenameTableCommand(BaseRenameTableCommand):
    def build_command(self):
        return f'ALTER TABLE {self.schema}."{self.table_name}" RENAME TO {self.schema}."{self.name}"'


PostgresMigrationDialect = {
    'create_table': PostgresCreateTableCommand,
    'alter_table': PostgresAlterTableCommand,
    'rename_table': PostgresRenameTableCommand,
}
