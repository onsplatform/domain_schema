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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._requirements = None

    @property
    def requirements(self):
        if not self._requirements:
            self._requirements = self.build_requirements()
        return self._requirements

    def build_requirements(self):
        """when overriden creates all the necessary requirements
           to allow us to create a new entity under test.

        :returns: dict
        """
        return {}

    def build(self):
        """builds the entity under test.

        :returns: MODEL instance.
        """
        create_data = self.create_data()
        data = {**create_data, **self.requirements}
        model = self.MODEL()
        nested = []

        for name, val in data.items():
            if name not in self.NESTED_MODELS:
                setattr(model, name, val)
                continue

            _type = self.NESTED_MODELS[name]
            entities = [_type(**v) for v in data[name]]
            nested.append((entities, getattr(model, name),))

        # we need to save the model first, otherwise django does not let us
        # update nested objects.
        model.save()
        for models, setter in nested:
            setter.set(models, bulk=False)

        # self.build_nested(model)
        return model


class ModelAPITestCase(SimpleAPITestCase,
                       ModelAPICreateTestMixin,
                       ModelAPIUpdateTestMixin,
                       ModelAPIQueryTestMixin):
    pass




