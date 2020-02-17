import django
from django.test import TransactionTestCase

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

    def test_get_dynamic_attribute(self):
        pass

    def test_get_dynamic_model(self):
        tests = [
            ["dummy1", "newobj2", True],
            ["dummy1", "newobj1", False],
            ["dummy2", "newobj2", True],
            ["dummy1", None, True],
        ]
        for test in tests:
            att = dynamic_model_utils.get_dynamic_attribute(*test[:2])
            self.assertIs(bool(att), test[2], f"{att} input: {test}")
