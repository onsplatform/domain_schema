import pytest

from domain_schema.celery import app


@pytest.fixture(scope='class')
def celery_app(request):
    app.conf.update(CELERY_ALWAYS_EAGER=True)
    request.cls.celery_app = app
