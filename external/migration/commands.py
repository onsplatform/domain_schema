class BaseTableManagement:
    """
    Base database table management command.
    When overridden should be able to manipulate tables.
    """
    def __init__(self, table_name):
        self.table_name = table_name

    def build(self):
        pass


class BaseTableStructureManagement(BaseTableManagement):
    """
    Base database table structure management command.
    When overridden should be able to manipulate a table along
    with it's structure, including columns, indexes, etc.
    """
    CONSTRAINTS = {}

    def __init__(self, *args):
        super().__init__(*args)
        self.columns = {}

    def _build_columns(self):
        for name, col in self.columns.items():
            constraints = [
                self.CONSTRAINTS.get(c)
                for c, v in col['constraints'].items() if v
            ]
            yield self._build_column(name, col['type'], constraints)

    def _build_column(self, name, _type, constraints):
        pass


class BaseCreateTableCommand(BaseTableStructureManagement):
    """
    Base database create table command.
    """
    SEPARATOR = ', '
    GROUP_START = '('
    GROUP_END = ')'
    DELIMITER = ';'

    def build(self):
        command = self.build_command()
        columns = str.join(', ', self._build_columns())
        return f'{command} {self.GROUP_START}{columns}{self.GROUP_END}{self.DELIMITER}'

    def with_column(self, name, _type, **constraints):
        self.columns[name] = {
            'type': _type,
            'constraints': constraints,
        }
        return self


class BaseRenameTableCommand(BaseTableManagement):
    """
    Base database rename table command.
    """
    def to(self, name):
        self.name = name
        return self

    def build(self):
        return self.build_command()
