# Create your tests here.
# Create your tests here.

import django
from django.test import TransactionTestCase

from json2model.services.dynamic_model import (
    create_instances_from_json,
    create_objects_from_json,
    get_dynamic_model
)


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
        create_objects_from_json("root_obj0", data)
        inst = create_instances_from_json("root_obj0", data)

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
        create_objects_from_json("root_obj1", data)
        instance = create_instances_from_json("root_obj1", data)

    def test_create_data_from_random_json(self):
        data = {
            "obj2": {
                "title": "title1",
                "obj3": {
                    "title": "title2"
                }
            }
        }
        create_objects_from_json("obj1", data)
        obj1 = create_instances_from_json("obj1", data)
        obj2 = get_dynamic_model("obj2").objects.first()
        obj3 = get_dynamic_model("obj3").objects.first()
        self.assertEqual(obj3.title, "title2")
        self.assertEqual(obj1.obj2.obj3.title, "title2")
