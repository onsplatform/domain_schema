import pytest
import json

from rest_framework.test import APIClient
from rest_framework.test import APITestCase


ASSERTION_MESSAGES = {
    'STATUS_CODE': "expected response code %i but got %i.",
    'OBJECT_EXISTS': 'expected %i existing object but there are %i.',
    'OBJECT_IN_RESPONSE': 'expected object with id %i missing in response.',
    'RESPONSE_LENGTH': 'expected %i objects in response, but it contains %i.',
    'FIELD_VALUE_EQUALS': 'expected object field %s to be equals to %s, but got %s.',
}

def assert_field_equality(resource, field_name, expected_value):
        assert resource.__dict__[field_name] == expected_value, \
            ASSERTION_MESSAGES['FIELD_VALUE_EQUALS'] % \
            (field_name, expected_value, resource.__dict__[key])


def assert_status_code(response, expected_code):
    """
    asserts request object has an expected status code.
    """
    assert response.status_code == expected_code, ASSERTION_MESSAGES['STATUS_CODE'] % (expected_code, response.status_code)


def assert_object_exists(cls, count=1):
    """
    asserts an object exists in the database.
    """
    total_count = cls.objects.count()
    assert total_count == count, ASSERTION_MESSAGES['OBJECT_EXISTS'] %  (count, total_count)


def assert_object_created(cls, response):
    """
    asserts an object was created in the database.
    """
    assert_status_code(response, 201 )
    assert_object_exists(cls)


def assert_response_contains_object(obj, response, is_array=True, max_count=1, status_code=200):
    """
    asserts a response object contains an existing object.
    """
    json_data = response.json()
    assert_status_code(response, status_code)

    if is_array:
        assert len(json_data) == max_count, ASSERTION_MESSAGES['RESPONSE_LENGTH'] % (max_count, len(json_data))
        json_data = json_data[0]

    assert obj.id == json_data['id'], ASSERTION_MESSAGES['OBJECT_IN_RESPONSE'] % obj.id


@pytest.fixture(scope='class')
def api_client(request):
    """
    django rest framework api client fixture.
    """
    request.cls.client = APIClient()


@pytest.fixture(scope='class')
def base_uri(request):
    """
    reverses model api to uri.
    this uri is based by convention in the name of the test class
    before TestCase.

    Ex.: MyModelTestCase will be wired to mymodel, so on, /api/mymodel.
    """
    uri_name = request.cls.__name__.replace('TestCase','').lower()
    request.cls.base_uri = f'/api/{uri_name}/'


@pytest.mark.usefixtures("base_uri")
@pytest.mark.usefixtures("api_client")
class ModelAPITestCase(APITestCase):
    MODEL = None
    __test__ = False

    def build_requirements(self):
        return {}

    def build(self):
        obj_data = self.create_data()
        obj_data.update(self.build_requirements())
        return self.MODEL.objects.create(**obj_data)

    def create_data(self):
        return {}

    def update_data(self):
        return {}

    def test_get_resources(self):
        # mock
        resource = self.build()

        # act
        response = self.client.get(self.base_uri)

        # assert
        assert_response_contains_object(resource, response)

    def test_create_resource(self):
        # mock
        obj_data = self.create_data()

        obj_data.update({
            f'{key}_id': val.id for key, val
            in self.build_requirements().items()
        })

        # act
        response = self.client.post(self.base_uri, obj_data, format='json')

        # assert
        assert_object_created(self.MODEL, response)

    def test_get_resource_by_key(self):
        resource = self.build()

        # act
        response = self.client.get(f'{self.base_uri}{resource.id}/')

        # assert
        assert_response_contains_object(resource, response, is_array=False)

    def test_update_resource(self):
        # mock
        resource = self.build()
        obj_data = self.update_data()
        obj_data.update({
            f'{k}_id': v.id for k, v in self.build_requirements().items()
        })

        # act
        response = self.client.put(
            f'{self.base_uri}{resource.id}/', obj_data, format='json')

        # assert
        updated_resource = self.MODEL.objects.get(pk=resource.id)

        for key, val in self.update_data().items():
            assert_field_equality(updated_resource, key, val)
