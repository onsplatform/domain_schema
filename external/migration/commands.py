class BaseTableManagementCommand:
    """
    Base database table management command.
    When overridden should be able to manipulate tables.
    """
    def __init__(self, table_name):
        self.table_name = table_name

    def build(self):
        pass


class BaseCreateTableCommand(BaseTableManagementCommand):
    """
    Base database create table command.
    """
    SEPARATOR = ', '
    GROUP_START = '('
    GROUP_END = ')'
    DELIMITER = ';'
    CONSTRAINTS = {}

    def __init__(self, *args):
        super().__init__(*args)
        self.columns = {}

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

    def _build_columns(self):
        for name, col in self.columns.items():
            constraints = [
                self.CONSTRAINTS.get(c)
                for c, v in col['constraints'].items() if v
            ]
            yield self._build_column(name, col['type'], constraints)

    def _build_column(self, name, _type, constraints):
        pass


class BaseAlterTableCommand(BaseTableManagementCommand):
    DELIMITER = ';'

    def __init__(self, *args):
        super().__init__(*args)
        self.add_columns = {}
        self.drop_columns = {}

    def build(self):
        command = self.build_command()
        add_columns = self._build_columns(self.add_columns)
        add_columns = str.join(', ', add_columns)
        return f'{command} {add_columns}{self.DELIMITER}'

    def add_column(self, name, _type, **constraints):
        self.add_columns[name] = {
            'type': _type,
            'constraints': constraints,
        }
        return self

    def _build_columns(self, columns):
        for name, col in columns.items():
            constraints = [
                self.CONSTRAINTS.get(c)
                for c, v in col['constraints'].items() if v
            ]
            yield self._build_column(name, col['type'], constraints)

    def _build_column(self, name, _type, constraints):
        pass


class BaseRenameTableCommand(BaseTableManagementCommand):
    """
    Base database rename table command.
    """
    def to(self, name):
        self.name = name
        return self

    def build(self):
        return self.build_command()
