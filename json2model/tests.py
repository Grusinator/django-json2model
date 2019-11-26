# Create your tests here.
# Create your tests here.
import unittest

import django
from django.test import TransactionTestCase


class TestDjangoDynamicModel(TransactionTestCase):
    """Tests for the application views."""

    # Django requires an explicit setup() when running tests in PTVS
    @classmethod
    def setUpClass(cls):
        super(TestDjangoDynamicModel, cls).setUpClass()
        django.setup()

    def test_simple(self):
        from .services import DynamicModelMutantService
        data = {"test4": {
            "dummy1": 1,
            "dummy2": "test2"
        }}
        instance = DynamicModelMutantService.create_from_data("test_root2", data)

        self.assertTrue(hasattr(instance, "test4"))
        self.assertTrue(hasattr(instance.test4, "dummy1"))
        self.assertTrue(hasattr(instance.test4, "dummy2"))
        self.assertEqual(instance.test4.dummy1, 1)
        self.assertEqual(instance.test4.dummy2, "test2")

    def test_many_to_many(self):
        from .services import DynamicModelMutantService
        data = {
            "prop2": 1,
            "prop1": "test2",
            "related_obj": [
                {
                    "name": "name1",
                    "value": 2
                },
                {
                    "name": "name2",
                    "value": 3
                },
            ]
        }
        instance = DynamicModelMutantService.create_from_data("root_obj", data)
        print(instance)

        self.assertTrue(hasattr(instance, "test4"))
        self.assertTrue(hasattr(instance.test4, "dummy1"))
        self.assertTrue(hasattr(instance.test4, "dummy2"))
        self.assertEqual(instance.test4.dummy1, 1)
        self.assertEqual(instance.test4.dummy2, "test2")
