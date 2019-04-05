import pytest
import json

from rest_framework.test import APIClient
from rest_framework.test import APITestCase


ASSERTION_MESSAGES = {
    'STATUS_CODE': "expected response code %i but got %i.",
    'OBJECT_EXISTS': 'expected %i existing object but there are %i.',
    'OBJECT_IN_RESPONSE': 'expected object with id %i missing in response.',
    'RESPONSE_LENGTH': 'expected %i objects in response, but it contains %i',
}


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


def assert_object_in_response(obj, response, max_count=1, status_code=200):
    """
    asserts a response object contains an existing object.
    """
    json_data = response.json()
    assert_status_code(response, status_code)
    assert len(json_data) == max_count, ASSERTION_MESSAGES['RESPONSE_LENGTH'] % (max_count, len(json_data))
    assert obj.id in {d['id'] for d in json_data}, ASSERTION_MESSAGES['OBJECT_IN_RESPONSE'] % obj.id


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
    pass
