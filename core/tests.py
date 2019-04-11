import pytest

from core.utils.testing import *
from core.models import Solution, App


class SolutionTestCase(ModelAPITestCase):
    def test_get_solutions(self):
        # mock
        sln = Solution.objects.create(name='test_solution')

        # act
        response = self.client.get(self.base_uri)

        # assert
        assert_object_in_response(sln, response)


    def test_create_solution(self):
        # act
        response = self.client.post(self.base_uri, {'name': 'test_solution'}, format='json')

        # assert
        assert_object_created(Solution, response)

class AppTestCase(ModelAPITestCase):
    def test_create_app(self):
        # act
        sln = Solution.objects.create(name='test_solution')
        response = self.client.post(self.base_uri, {'name': 'test_app', 'solution_id': sln.id}, format='json')

        # assert
        assert_object_created(App, response)
