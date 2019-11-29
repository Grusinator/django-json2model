# Create your tests here.
# Create your tests here.

import django
from django.test import TransactionTestCase

from json2model.services.dynamic_model import get_dynamic_model, create_objects_from_json


class TestDjangoDynamicModel(TransactionTestCase):
    """Tests for the application views."""

    # Django requires an explicit setup() when running tests in PTVS
    @classmethod
    def setUpClass(cls):
        super(TestDjangoDynamicModel, cls).setUpClass()
        django.setup()

    def test_create_dynamic_simple(self):

        data = {
            "desc": "some",
            "relate": {
                "dummy1": 1,
                "dummy2": "value1"
            }
        }
        Object = create_objects_from_json("main", data)

        inst = Object(desc="soemthing")
        inst.save()
        Objrelate = get_dynamic_model("relate")
        inst2 = Objrelate(main=inst, dummy1=2, dummy2="value2")
        inst2.save()

        self.assertTrue(hasattr(inst, "relate"))
        self.assertTrue(hasattr(inst.relate, "dummy1"))
        self.assertTrue(hasattr(inst.relate, "dummy2"))
        self.assertEqual(inst.relate.dummy1, 2)
        self.assertEqual(inst.relate.dummy2, "value2")

    def test_create_dynamic_list_of_objects(self):
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

    def test_create_random_json(self):
        data = {
            "glossary": {
                "title": "example glossary",
                "GlossDiv": {
                    "title": "S",
                    "GlossList": {
                        "GlossEntry": {
                            "ID": "SGML",
                            "SortAs": "SGML",
                            "GlossTerm": "Standard Generalized Markup Language",
                            "Acronym": "SGML",
                            "Abbrev": "ISO 8879:1986",
                            "GlossDef": {
                                "para": "A meta-markup language, used to create markup languages such as DocBook.",
                                "GlossSeeAlso": ["GML", "XML"]
                            },
                            "GlossSee": "markup"
                        }
                    }
                }
            }
        }
        Object = create_objects_from_json("root_obj2", data)
        Obj1 = get_dynamic_model("GlossEntry")
        Obj2 = get_dynamic_model("GlossList")
        Obj3 = get_dynamic_model("glossary")

