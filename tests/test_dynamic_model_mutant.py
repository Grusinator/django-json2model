from unittest.mock import Mock

import pytest
from django.db import IntegrityError

from json2model.services.dynamic_model.dynamic_model_builder import DynamicModelBuilder
from json2model.services.dynamic_model.dynamic_model_utils import get_dynamic_model
from tests.attribute_that_fails import make_attributes_with_value_0_fail


class TestDynamicModelMutant:

    @pytest.mark.django_db
    def test_create_dynamic_simple(self):
        data = {
            "desc": "some",
            "relate": {
                "dummy1": 1,
                "dummy2": "value1"
            }
        }

        root_name = "model_test0"
        model_builder = DynamicModelBuilder()
        Object = model_builder.create_models_from_data(root_name, data)

        inst = Object(desc="soemthing")
        inst.save()
        Objrelate = get_dynamic_model("relate")
        inst2 = Objrelate(model_test0=inst, dummy1=2, dummy2="value2")
        inst2.save()

        assert hasattr(inst, "relate")
        assert hasattr(inst.relate, "dummy1")
        assert hasattr(inst.relate, "dummy2")
        assert inst.relate.dummy1 == 2
        assert inst.relate.dummy2 == "value2"

    @pytest.mark.django_db
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
        root_name = "model_test1"
        model_builder = DynamicModelBuilder()
        ModelObject = model_builder.create_models_from_data(root_name, data)

        instance = ModelObject(prop2=3)
        instance.save()

        # instance_builder = DynamicDataInstances()
        # instances = instance_builder.create_instances_from_data(root_name, data)

        RelObj = get_dynamic_model("related_obj")
        inst1 = RelObj(name="Peter Meyer", value=3, model_test1=instance)
        inst1.save()
        inst1 = RelObj(name="Anders Rikvold", value=3, model_test1=instance)
        inst1.save()

    @pytest.mark.django_db
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

        root_name = "model_test2"
        model_builder = DynamicModelBuilder()
        model_builder.create_models_from_data(root_name, data)

        # TODO validate here
        # self.fail()

    @pytest.mark.django_db
    def test_error_in_create_attribute_does_not_propagate(self):
        DynamicModelBuilder._get_or_create_attribute = Mock()
        DynamicModelBuilder._get_or_create_attribute.side_effect = IntegrityError("Booom!!")
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
        ModelObject = model_builder.create_models_from_data(root_name, data)
        assert len(model_builder.failed_objects) == 1

    @pytest.mark.django_db
    def test_if_list_of_objects_with_some_errors_are_caught_correctly(self):
        data = {
            "newobj3": {
                "related2": [
                    {
                        "attribute": 0,
                    },
                    {
                        "attribute": 1,
                    },
                    {
                        "attribute": 0,
                    },
                    {
                        "attribute": 1,
                    }
                ]
            }
        }

        root_name = "model_test4"
        model_builder = DynamicModelBuilder()
        model_builder.handle_attribute = Mock(side_effect=make_attributes_with_value_0_fail)
        ModelObject = model_builder.create_models_from_data(root_name, data)
        assert len(model_builder.failed_objects) == 2
        relatedOb = get_dynamic_model("related2")
        assert relatedOb is not None
