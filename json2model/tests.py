# Create your tests here.
# Create your tests here.

import django
from django.test import TransactionTestCase

from json2model.services.dynamic_model import get_dynamic_model


class TestDjangoDynamicModel(TransactionTestCase):
    """Tests for the application views."""

    # Django requires an explicit setup() when running tests in PTVS
    @classmethod
    def setUpClass(cls):
        super(TestDjangoDynamicModel, cls).setUpClass()
        django.setup()

    def test_create_dynamic_simple(self):
        from .services.dynamic_model import create_objects_from_json
        data = {"test4": {
            "dummy1": 1,
            "dummy2": "value1"
        }}
        Object = create_objects_from_json("test_root3", data)

        inst = Object()
        ObjTest4 = get_dynamic_model("test4")
        inst2 = ObjTest4(dummy1=2, dummy2="value2")
        inst2.save()
        inst.test4 = inst2
        inst.save()

        self.assertTrue(hasattr(inst, "test4"))
        self.assertTrue(hasattr(inst.test4, "dummy1"))
        self.assertTrue(hasattr(inst.test4, "dummy2"))
        self.assertEqual(inst.test4.dummy1, 2)
        self.assertEqual(inst.test4.dummy2, "value2")

    def test_create_dynamic_list_of_objects(self):
        from .services.dynamic_model import create_objects_from_json
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
        Object = create_objects_from_json("root_obj", data)
        instance = Object(prop2=3)
        instance.save()
        RelObj = get_dynamic_model("related_obj")
        inst1 = RelObj(name="Peter Meyer", value=3, root_obj=instance)
        inst1.save()
        inst1 = RelObj(name="Anders Rikvold", value=3, root_obj=instance)
        inst1.save()
        #
        # self.assertTrue(hasattr(instance, "test4"))
        # self.assertTrue(hasattr(instance.test4, "dummy1"))
        # self.assertTrue(hasattr(instance.test4, "dummy2"))
        # self.assertEqual(instance.test4.dummy1, 1)
        # self.assertEqual(instance.test4.dummy2, "test2")
