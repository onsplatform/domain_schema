from core.utils.testing import *

from core.models import Solution, App, Migration, Entity, \
        Field, EntityMap, MappedField, FIELD_TYPES


# class SolutionTestCase(ModelAPITestCase):
#     MODEL = Solution
#     __test__ = True

#     def update_data(self):
#         return {
#             'name': 'test_solution_upd'
#         }

#     def create_data(self):
#         return {
#             'name': 'test_solution'
#         }


# class AppTestCase(ModelAPITestCase):
#     MODEL = App
#     __test__ = True

#     def build_requirements(self):
#         return {
#             'solution': Solution.objects.create(name='test_solution')
#         }

#     def create_data(self):
#         return {
#             'name': 'test_app'
#         }

#     def update_data(self):
#         return {
#             'name': 'test_app_upd'
#         }


class EntityTestCase(ModelAPITestCase):
    MODEL = Entity
    NESTED_MODELS = {'fields': Field}
    __test__ = True

    def build_requirements(self):
        return {
            'solution': Solution.objects.create(name='test_solution'),
        }

    def create_data(self):
        return {
            'name': 'test_entity',
            'table': 'test_table',
            'fields': [{
                'name': 'test_field',
                'field_type': 'char',
            }]
        }

    def update_data(self):
        return {
            'name': 'test_entity_upd',
            'table': 'test_table',
            'fields': [{
                'name': 'test_field_a',
                'field_type': 'char',
            }]
        }


# class EntityMapTestCase(ModelAPITestCase):
#     MODEL = EntityMap
#     NESTED_MODELS = {
#         'fields': MappedField,
#     }
#     __test__ = True

#     def build_requirements(self):
#         sln = Solution.objects.create(name='test_solution')
#         app = App.objects.create(name='test_app', solution=sln)
#         entity = Entity.objects.create(
#             name='test_entity', solution=sln, table='tb_test_entity')

#         return {
#             'entity': entity,
#             'app': app,
#         }

#     def create_data(self):
#         field  = Field.objects.create(
#             entity=self.requirements['entity'],
#             name='test_field',
#             field_type=FIELD_TYPES.INTEGER)

#         return {
#             'name': 'test_map',
#             'app_id': self.requirements['app'].id,
#             'entity_id': self.requirements['entity'].id,
#             'fields': [{
#                 'field_id': field.id,
#                 'alias': 'test_alias',
#             }]
#         }

#     def update_data(self):
#         field  = Field.objects.create(
#             entity=self.requirements['entity'],
#             name='test_field',
#             field_type=FIELD_TYPES.INTEGER)

#         return {
#             'name': 'test_map_upd',
#             'fields': [{
#                 'field_id': field.id,
#                 'alias': 'test_alias',
#             }]
#         }
