import django
from django.test import TransactionTestCase

from json2model.services.dynamic_model import DynamicModelBuilder, DynamicDataInstances
from json2model.services.dynamic_model.dynamic_model_utils import get_dynamic_model, add_prefix_to_model_label


class TestModelNamePrefix(TransactionTestCase):
    """Tests for the application views."""

    # Django requires an explicit setup() when running tests in PTVS
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        django.setup()

    def test_simple(self):
        related_name = "relate26"
        data = {
            "desc": "some",
            related_name: {
                "dummy1": 1,
                "dummy2": "value1"
            }
        }

        prefix = "provider"
        root_name = "model_test26"
        model_builder = DynamicModelBuilder(model_name_prefix=prefix)
        model_builder.create_models_from_data(data, root_name)
        Object = get_dynamic_model(root_name)
        Objrelate = get_dynamic_model(related_name)
        prefixed_related_name = add_prefix_to_model_label(related_name, prefix)
        self.assertEqual(Object.__name__, add_prefix_to_model_label(root_name, prefix))
        self.assertEqual(Objrelate.__name__, prefixed_related_name)

        instance_builder = DynamicDataInstances(model_name_prefix=prefix)
        inst = instance_builder.create_instances_from_data(data, root_name)

        rel_inst = getattr(inst, prefixed_related_name)
        self.assertTrue(hasattr(inst, prefixed_related_name))
        self.assertTrue(hasattr(rel_inst, "dummy1"))
        self.assertEqual(rel_inst.dummy1, 1)
        self.assertEqual(rel_inst.dummy2, "value1")
