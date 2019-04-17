from rest_framework.test import APITestCase

from .assertions import *
from .fixtures import *
from .mixins import *


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








