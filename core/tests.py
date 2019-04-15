import pytest

from core.utils.testing import *
from core.models import Solution, App, Entity, Field, FIELD_TYPES


class SolutionTestCase(ModelAPITestCase):
    MODEL = Solution
    __test__ = True

    def update_data(self):
        return {
            'name': 'test_solution_upd'
        }

    def create_data(self):
        return {
            'name': 'test_solution'
        }


class AppTestCase(ModelAPITestCase):
    MODEL = App
    __test__ = True

    def build_requirements(self):
        return {
            'solution': Solution.objects.create(name='test_solution')
        }

    def create_data(self):
        return {
            'name': 'test_app'
        }

    def update_data(self):
        return {
            'name': 'test_app_upd'
        }


class EntityTestCase(ModelAPITestCase):
    MODEL = Entity
    __test__ = True

    def build_requirements(self):
        return {
            'solution': Solution.objects.create(name='test_solution')
        }

    def create_data(self):
        return {
            'name': 'test_entity'
        }

    def update_data(self):
        return {
            'name': 'test_entity_upd'
        }
