from django.apps import AppConfig


class Json2ModelConfig(AppConfig):
    name = 'json2model'

    # def ready(self):
    #     from json2model.services.dynamic_model import DynamicModelMutant
    #     DynamicModelMutant.register_all_models()

