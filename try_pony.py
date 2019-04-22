from pony import orm


db = orm.Database()


class RemoteField:
    def __init__(self, name, field_type, column, required=True):
        self.name = name
        self.field_type = field_type
        self.column = column
        self.required = required

    def build(self):
        wrapper = orm.Required if self.required else orm.Optional
        return wrapper(self.field_type, column=self.column)


class RemoteMap:
    def __init__(self, name, table, fields):
        self.name = name
        self.table = table
        self.fields = fields

    def build(self):
        fields = { f.name: f.build() for f in self.fields }
        fields['_table_'] = self.table
        dyn_type = type(self.name, (db.Entity, ), fields)
        return dyn_type


if __name__ == "__main__":
    # this would come from domain schema.
    person_map = RemoteMap('Person', 'tb_1', [
        RemoteField('name', str, 'c1'),
        RemoteField('age', int, 'c2')
    ])

    # build a dynamic pony class from remote map.
    Person = person_map.build()

    # registering map in pony
    db.bind(provider='sqlite', filename='database.sqlite', create_db=True)
    db.generate_mapping(create_tables=True)

    # querying data
    with orm.db_session():
        person = Person(name='Foo', age=23)
        # create entity
        # d1 = dyn_mapping(name='Foo', age='10')
        orm.commit()

        # query entities
        people = orm.select(d for d in Person)

        for p in people:
            print(p.name, p.age)

