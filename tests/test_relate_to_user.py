import django
from django.contrib.auth.models import User
from django.test import TransactionTestCase

from json2model.services.dynamic_model import DynamicModelBuilder
from json2model.services.dynamic_model import dynamic_model_builder
from json2model.services.dynamic_model.dynamic_model_builder import get_or_create_user_model_def
from test_app.models import Dummy


class TestRelateToUser(TransactionTestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        django.setup()
        setattr(dynamic_model_builder, "RELATE_TO_USER", True)

    def test_get_or_create_user_model_def(self):
        Dummy.objects.create(dummy_field="test")
        model_def = get_or_create_user_model_def()
        self.assertIsNotNone(model_def)

    def test_relate_to_user(self):
        data = {
            "prop2": 1,
        }
        user = User.objects.create(username="guest", password="dev1234")
        root_name = "model_test8"
        model_builder = DynamicModelBuilder()
        ModelObject = model_builder.create_models_from_data(root_name, data)
        inst = ModelObject.objects.create(prop2=3, user=user)
