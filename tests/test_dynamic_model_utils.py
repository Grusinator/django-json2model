import unittest

import django
from django.test import TransactionTestCase
from mutant.contrib.numeric.models import BigIntegerFieldDefinition
from mutant.contrib.text.models import TextFieldDefinition

from json2model.services.dynamic_model import dynamic_model_utils
from json2model.services.dynamic_model.dynamic_model_builder import DynamicModelBuilder


class TestDynamicModelUtils(TransactionTestCase):
    """Tests for the application views."""

    # Django requires an explicit setup() when running tests in PTVS
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        django.setup()
        data = {
            "newobj1": {
                "newobj2": {
                    "dummy1": 1,
                    "dummy2": "value1"
                }
            }
        }
        root_name = "model_test3"
        model_builder = DynamicModelBuilder()
        model_builder.create_models_from_data(data, root_name)

    @unittest.skip("idk")
    def test_get_dynamic_model(self):
        obj = dynamic_model_utils.get_dynamic_model("newobj1")
        self.assertIsNotNone(obj)

    def test_get_dynamic_attribute(self):
        tests = [
            ["dummy1", "newobj2", BigIntegerFieldDefinition],
            ["dummy1", "newobj1", type(None)],
            ["dummy2", "newobj2", TextFieldDefinition],
            ["dummy1", None, BigIntegerFieldDefinition],
        ]
        for test in tests:
            att = dynamic_model_utils.get_dynamic_attribute(*test[:2])
            self.assertEqual(type(att), test[2], f"{att} input: {test}")
