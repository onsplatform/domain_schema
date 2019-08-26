from .assertions import *


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
            in self.requirements.items()
        })

        # act
        response = self.client.post(self.base_uri, obj_data, format='json')

        # assert
        assert_object_created(self.MODEL, response)

        # load created entity
        entity = self.MODEL.objects.get(pk=response.json()['id'])

        # let the user create it's own assertions
        self.assert_after_create(entity)

    def assert_after_create(self, entity):
        """when overridden allows user to make custom assertions.
           runs after the entity is persisted in the database.
        """
        pass


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
        # __import__('ipdb').set_trace()
        resource = self.build()
        update_data = self.update_data()
        obj_data = {
            **update_data,
            **{f'{k}_id': v.id for k, v in self.requirements.items()}
        }

        # act
        response = self.client.put(
            f'{self.base_uri}{resource.id}/', obj_data, format='json')

        # assert
        updated_resource = self.MODEL.objects.get(pk=resource.id)

        for key, val in update_data.items():
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

