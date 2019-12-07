import logging
from importlib import import_module, reload

from django.contrib import admin
from django.contrib.admin.sites import NotRegistered
from django.urls import clear_url_caches
from mutant.models import ModelDefinition

from django_json2model import settings

logger = logging.getLogger(__name__)
APP_LABEL = settings.APP_LABEL_DYNAMIC_MODELS


def register_all_models():
    model_defs = ModelDefinition.objects.filter(app_label=APP_LABEL)
    for model_def in model_defs:
        try:
            register_model_in_admin(model_def)
        except admin.sites.AlreadyRegistered:
            pass
    reload_and_clear_cache_admin()


def register_model_in_admin(model_def):
    ObjectModel = model_def.model_class()
    attrs = {'model': ObjectModel}
    ObjectModelAdmin = type(f'{ObjectModel.__name__}Admin', (admin.ModelAdmin,), attrs)
    admin.site.register(ObjectModel, ObjectModelAdmin)


def try_unregister_model_in_admin(model_def):
    ObjectModel = model_def.model_class()
    try:
        admin.site.unregister(ObjectModel)
        reload_and_clear_cache_admin()
    except NotRegistered:
        logger.warning(f"model_def: {model_def.name}, was not registered in admin.site, "
                       f"and could therefore not unregister")


def reload_and_clear_cache_admin():
    reload(import_module(settings.ROOT_URLCONF))
    clear_url_caches()
