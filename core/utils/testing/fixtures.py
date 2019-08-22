import pytest

from rest_framework.test import APIClient


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
    request.cls.base_uri = f'/api/v1/{uri_name}/'
