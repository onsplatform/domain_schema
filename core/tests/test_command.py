import pytest

from django.test import TestCase

from core.models import Solution, App, Migration, Entity, \
        Field, EntityMap, MappedField, FIELD_TYPES
from core.utils import postgres as pg
from core.tasks import apply_model_migration


class CommandTestCase(TestCase):
    def test_execute_import_data(self):
 
        assert  1 == 2
     

  