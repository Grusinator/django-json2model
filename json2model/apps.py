import logging

from django.apps import AppConfig

logger = logging.getLogger(__name__)


class Json2ModelConfig(AppConfig):
    name = 'json2model'

    def ready(self):
        import json2model.services.dynamic_model.dynamic_model_admin_handler as admin_handler
        try:
            admin_handler.register_all_models()
        except Exception as e:
            logger.warning("models could not be registered in admin due to error:" + str(e))
