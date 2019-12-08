from django.apps import AppConfig


class Json2ModelConfig(AppConfig):
    name = 'json2model'

    def ready(self):
        import json2model.services.dynamic_model.dynamic_model_admin_handler as admin_handler
        admin_handler.register_all_models()
