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
        (field_name, expected_value, resource.__dict__[field_name])


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


class ModelAPICreateTestMixin:
    """Test mixing for model creating endpoints. """

    def create_data(self):
        """must be overridden with the desired data which will be sent
           in the body of the http request to test creating an entity.

           :return dict.
        """
        return {}

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


class ModelAPIUpdateTestMixin:
    """Test mixing for model updating endpoints. """

    def update_data(self):
        """must be overridden with the desired data which will be sent
           in the body of the http request to test updating an entity.

           :return dict.
        """
        return {}

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
            if key not in self.NESTED_MODELS:
                assert_field_equality(updated_resource, key, val)


class ModelAPIQueryTestMixin:
    """Test mixing for model querying endpoints. """

    def test_get_resources(self):
        # mock
        resource = self.build()

        # act
        response = self.client.get(self.base_uri)

        # assert
        assert_response_contains_object(resource, response)

    def test_get_resource_by_key(self):
        # mock
        resource = self.build()

        # act
        response = self.client.get(f'{self.base_uri}{resource.id}/')

        # assert
        assert_response_contains_object(resource, response, is_array=False)


@pytest.mark.usefixtures("base_uri")
@pytest.mark.usefixtures("api_client")
class SimpleAPITestCase(APITestCase):
    MODEL = None
    NESTED_MODELS = {}
    __test__ = False

    def build_requirements(self):
        """when overriden creates all the necessary requirements
           to allow us to create a new entity under test.

        :returns: dict
        """
        return {}

    def build_nested(self, model):
        """builds and loads nested objects in the entity under test.
        """
        for name, _type in self.NESTED_MODELS.items():
            nested_attr = getattr(model, name, None)

            if not nested_attr:
                continue

            data = self.create_data()
            entities = [_type(**v) for v in data[name]]
            nested_attr.set(entities, bulk=False)

    def build(self):
        """builds the entity under test.

        :returns: MODEL instance.
        """
        data = {**self.create_data(), **self.build_requirements()}
        model = self.MODEL()

        for key, val in data.items():
            if key not in self.NESTED_MODELS:
                setattr(model, key, val)

        model.save()
        self.build_nested(model)
        return model


class ModelAPITestCase(SimpleAPITestCase,
                       ModelAPICreateTestMixin,
                       ModelAPIUpdateTestMixin,
                       ModelAPIQueryTestMixin):
    pass








