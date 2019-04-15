import pytest

from core.utils.testing import *
from core.models import Solution, App, Entity, Field, FIELD_TYPES


class SolutionTestCase(ModelAPITestCase):
    def test_get_solutions(self):
        # mock
        sln = Solution.objects.create(name='test_solution')

        # act
        response = self.client.get(self.base_uri)

        # assert
        assert_response_contains_object(sln, response)


    def test_create_solution(self):
        # act
        response = self.client.post(self.base_uri, {'name': 'test_solution'}, format='json')

        # assert
        assert_object_created(Solution, response)


class AppTestCase(ModelAPITestCase):
    def test_create_app(self):
        # mock
        sln = Solution.objects.create(name='test_solution')

        # act
        response = self.client.post(self.base_uri, {'name': 'test_app', 'solution_id': sln.id}, format='json')

        # assert
        assert_object_created(App, response)


class EntityTestCase(ModelAPITestCase):
    def test_create_entity(self):
        # mock
        sln = Solution.objects.create(name='test_solution')

        #act
        response = self.client.post(
            self.base_uri,
            {'name': 'test_entity', 'solution_id': sln.id},
            format='json')

        #assert
        assert_object_created(Entity, response)

    def test_get_entities(self):
        # mock
        solution = Solution.objects.create(name='test_solution')
        entity = Entity.objects.create(name='test_entity', solution=solution)

        # act
        response = self.client.get(self.base_uri)

        # assert
        assert_response_contains_object(solution, response)

    def test_get_entity_by_key(self):
        # mock
        solution = Solution.objects.create(name='test_solution')
        entity = Entity.objects.create(name='test_entity', solution=solution)
        field = Field.objects.create(
            name='test_field', entity=entity, field_type=FIELD_TYPES.CHAR)

        # act
        response = self.client.get(f'{self.base_uri}{entity.id}/')
        json_response = response.json()

        # assert
        assert_response_contains_object(entity, response, is_array=False)

        assert 'fields' in json_response
        assert json_response['fields'][0]['id'] == field.id
