import unittest
from unittest.mock import Mock, patch

import django
from django.contrib.auth.models import User
from django.test import TransactionTestCase

from json2model.services.dynamic_model import DynamicModelBuilder, DynamicDataInstances
from json2model.services.dynamic_model import dynamic_model_builder, dynamic_data_instances
from json2model.services.dynamic_model.dynamic_model_utils import get_dynamic_model
from test_app.models import Dummy


class TestRelateToUser(TransactionTestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        django.setup()
        setattr(dynamic_model_builder, "RELATE_TO_USER", True)
        setattr(dynamic_data_instances, "RELATE_TO_USER", True)
        cls.user = User.objects.create(username="guest", password="dev1234")

    @unittest.skip
    def test_get_or_create_user_model_def(self):
        Dummy.objects.create(dummy_field="test")
        # model_def = create_user_model_def()
        # self.assertIsNotNone(model_def)

    def test_build_model_with_user_pk(self):
        data = {
            "prop2": 1,
        }
        root_name = "user_test_1"
        model_builder = DynamicModelBuilder()
        model_builder.create_models_from_data(root_name, data)
        ModelObject = get_dynamic_model(root_name)
        inst = ModelObject.objects.create(prop2=3, user_pk=self.user.pk)

    @patch("json2model.services.dynamic_model.dynamic_data_instances.DynamicDataInstances.relate_object_to_user",
           Mock())
    def test_relate_object_to_user_being_called(self):
        data = {
            "obj221": {
                "title": "title324",
            }
        }
        root_name = "user_test2"
        model_builder = DynamicModelBuilder()
        model_builder.create_models_from_data(root_name, data)
        self.assertTrue(len(model_builder.failed_objects) is 0)
        instance_builder = DynamicDataInstances(self.user.pk)
        instances = instance_builder.create_instances_from_data(root_name, data)
        self.assertTrue(DynamicDataInstances.relate_object_to_user.called)

    def test_instances_are_being_assigned(self):
        data = {
            "obj22": {
                "title": "title324",
            }
        }
        root_name = "user_test3"
        model_builder = DynamicModelBuilder()
        model_builder.create_models_from_data(root_name, data)
        self.assertTrue(len(model_builder.failed_objects) is 0)
        instance_builder = DynamicDataInstances(self.user.pk)
        instances = instance_builder.create_instances_from_data(root_name, data)
        obj2 = get_dynamic_model("obj22").objects.first()
        self.assertEqual(obj2.user_pk, self.user.pk)

    def test_instances_are_being_assigned_nested(self):
        data = {
            "obj55": {
                "title8": "title32",
                "obj66": {
                    "title7": "title44"
                }
            }
        }
        root_name = "user_test4"
        model_builder = DynamicModelBuilder()
        model_builder.create_models_from_data(root_name, data)

        instance_builder = DynamicDataInstances(self.user.pk)
        instances = instance_builder.create_instances_from_data(root_name, data)
        obj2 = get_dynamic_model("obj55").objects.first()
        obj3 = get_dynamic_model("obj66").objects.first()
        self.assertEqual(obj3.user_pk, self.user.pk)
        self.assertEqual(obj2.user_pk, self.user.pk)
