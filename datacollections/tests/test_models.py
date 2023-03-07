from django.core.exceptions import ValidationError
from django.test import TestCase

from datacollections.models import DataSet


class ItemModelTest(TestCase):

    def test_cannot_save_empty_item(self):
        pass

    def test_duplicate_items_are_invalid(self):
        pass

    def test_string_representation(self):
        pass

    def test_representation(self):
        pass
