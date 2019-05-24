class DatabaseMigration:
    def __init__(self, dialect):
        self.dialect = dialect

    def create_table(self, table_name, schema='public'):
        return self.dialect['create_table'](table_name, schema)

    def alter_table(self, table_name, schema='public'):
        return self.dialect['alter_table'](table_name, schema)

    def rename_table(self, table_name, schema='public'):
        return  self.dialect['rename_table'](table_name, schema)

