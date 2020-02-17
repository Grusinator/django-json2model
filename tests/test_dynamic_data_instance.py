import django
from django.test import TransactionTestCase

from json2model.services.dynamic_model import DynamicModelBuilder, DynamicDataInstances
from json2model.services.dynamic_model.dynamic_model_utils import get_dynamic_model


class TestDynamicModelMutant(TransactionTestCase):
    """Tests for the application views."""

    # Django requires an explicit setup() when running tests in PTVS
    @classmethod
    def setUpClass(cls):
        super(TestDynamicModelMutant, cls).setUpClass()
        django.setup()

    # def tearDown(self) -> None:
    #     delete_all_dynamic_models()

    def test_create_dynamic_data_simple(self):
        data = {
            "desc": "some",
            "relate1": {
                "dummy1": 1,
                "dummy2": "value1"
            }
        }
        root_name = "instance_test0"
        model_builder = DynamicModelBuilder()
        model_builder.create_models_from_data(root_name, data)
        instance_builder = DynamicDataInstances()
        inst = instance_builder.create_instances_from_data(root_name, data)

        self.assertTrue(hasattr(inst, "relate1"))
        self.assertTrue(hasattr(inst.relate1, "dummy1"))
        self.assertEqual(inst.relate1.dummy1, 1)
        self.assertEqual(inst.relate1.dummy2, "value1")

    def test_create_data_dynamic_list_of_objects(self):
        data = {
            "prop2": 1,
            "prop1": "test2",
            "related_obj1": [
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
        root_name = "instance_test1"
        model_builder = DynamicModelBuilder()
        model_builder.create_models_from_data(root_name, data)

        instance_builder = DynamicDataInstances()
        instances = instance_builder.create_instances_from_data(root_name, data)

    def test_create_data_from_random_json(self):
        data = {
            "obj2": {
                "title": "title1",
                "obj3": {
                    "title": "title2"
                }
            }
        }
        root_name = "instance_test2"
        model_builder = DynamicModelBuilder()
        model_builder.create_models_from_data(root_name, data)

        instance_builder = DynamicDataInstances()
        instances = instance_builder.create_instances_from_data(root_name, data)
        obj2 = get_dynamic_model("obj2").objects.first()
        obj3 = get_dynamic_model("obj3").objects.first()
        self.assertEqual(obj3.title, "title2")
        self.assertEqual(obj2.title, "title1")
