class DatabaseMigration:
    def __init__(self, dialect):
        self.dialect = dialect

    def create_table(self, table_name):
        return self.dialect.create_table(table_name)

    def alter_table(self, table_name):
        return self.dialect.alter_table(table_name)

    def rename_table(self, table_name):
        return  self.dialect.rename_table(table_name)

