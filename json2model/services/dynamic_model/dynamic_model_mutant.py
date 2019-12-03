import datetime
import logging
from abc import ABC
from importlib import import_module, reload

import mutant.contrib.boolean.models
import mutant.contrib.file.models
import mutant.contrib.numeric.models
import mutant.contrib.related.models
import mutant.contrib.temporal.models
import mutant.contrib.text.models
from django.contrib import admin
from django.contrib.admin.sites import NotRegistered
from django.contrib.sessions.backends import file
from django.core.exceptions import MultipleObjectsReturned
from django.urls import clear_url_caches
from mutant.models import ModelDefinition

from django_json2model import settings
from json2model.services.dynamic_model.i_json_iterator import IJsonIterator
from json2model.utils import except_errors

logger = logging.getLogger(__name__)


def create_objects_from_json(root_name, data):
    return DynamicModelMutant.create_models_from_data(root_name, data)


def get_dynamic_model(model_name: str):
    return DynamicModelMutant.get_dynamic_model(model_name)


def delete_dynamic_model(model_name: str):
    DynamicModelMutant.delete_dynamic_model(model_name)


def delete_all_dynamic_models(**filter_kwargs):
    DynamicModelMutant.delete_all_dynamic_models(**filter_kwargs)


class DynamicModelMutant(IJsonIterator, ABC):
    ATTRIBUTE_TYPES = {
        str: mutant.contrib.text.models.TextFieldDefinition,
        float: mutant.contrib.numeric.models.FloatFieldDefinition,
        bool: mutant.contrib.boolean.models.BooleanFieldDefinition,
        int: mutant.contrib.numeric.models.BigIntegerFieldDefinition,
        file: mutant.contrib.file.models.FilePathFieldDefinition,
        datetime: mutant.contrib.temporal.models.DateTimeFieldDefinition,
        # ('varchar', mutant.contrib.text.models.CharFieldDefinition),
        #
        # ('integer', mutant.contrib.numeric.models.BigIntegerFieldDefinition),
        # ('small_integer', mutant.contrib.numeric.models.SmallIntegerFieldDefinition),
        # ('float', mutant.contrib.numeric.models.FloatFieldDefinition),
        #
        # ('null_boolean', mutant.contrib.boolean.models.NullBooleanFieldDefinition),
        # ('boolean', mutant.contrib.boolean.models.BooleanFieldDefinition),
        #
        # ('file', mutant.contrib.file.models.FilePathFieldDefinition),
        #
        # ('foreign_key', mutant.contrib.related.models.ForeignKeyDefinition),
        # ('one_to_one', mutant.contrib.related.models.OneToOneFieldDefinition),
        # ('many_to_many', mutant.contrib.related.models.ManyToManyFieldDefinition),
        #
        # ('ip_generic', mutant.contrib.web.models.GenericIPAddressFieldDefinition),
        # ('ip', mutant.contrib.web.models.IPAddressFieldDefinition),
        # ('email', mutant.contrib.web.models.EmailFieldDefinition),
        # ('url', mutant.contrib.web.models.URLFieldDefinition),
        #
        # ('date', mutant.contrib.temporal.models.DateFieldDefinition),
        # ('time', mutant.contrib.temporal.models.TimeFieldDefinition),
        # ('datetime', mutant.contrib.temporal.models.DateTimeFieldDefinition),
    }
    RELATION_TYPES = {
        False: mutant.contrib.related.models.OneToOneFieldDefinition,
        True: mutant.contrib.related.models.ForeignKeyDefinition
    }
    APP_LABEL = "dynamicmodels"

    @classmethod
    def create_models_from_data(cls, root_label, data):
        object_name = cls._iterate_data_structure(data, object_label=root_label)
        cls.register_all_models()
        return cls.get_dynamic_model(object_name)

    @classmethod
    def get_dynamic_model(cls, model_name):
        return cls._get_model_def(model_name).model_class()

    @classmethod
    def delete_all_dynamic_models(cls, **filter_kwargs):
        model_defs = ModelDefinition.objects.filter(**filter_kwargs)
        [cls._delete_dynamic_model(model_def) for model_def in model_defs]

    @classmethod
    def delete_dynamic_model(cls, model_name: str):
        model_def = cls._get_model_def(model_name)
        cls._delete_dynamic_model(model_def)

    @classmethod
    def _delete_dynamic_model(cls, model_def):
        cls.try_unregister_model_in_admin(model_def)
        cls.delete_attribute_defs(model_def)
        cls.delete_relation_defs(model_def)
        model_def.delete()
        return model_def


    @classmethod
    def handle_attribute(cls, object_ref, attribute_label, data):
        if isinstance(data, list):
            # TODO this should be done better
            data = str(data)
        model_def = cls._get_model_def(object_ref)
        SpecificFieldDefinition = cls._get_specific_field_def(data)
        field_schema, created = SpecificFieldDefinition.objects.get_or_create(
            name=attribute_label,
            model_def=model_def,
            blank=True,
            null=True
        )
        return field_schema

    @classmethod
    @except_errors
    def pre_handle_object(cls, parent_ref, object_label, data):
        model_def, created = ModelDefinition.objects.get_or_create(
            app_label=cls.APP_LABEL,
            object_name=object_label,
            defaults={'fields': []},
        )
        return object_label

    @classmethod
    def post_handle_object(cls, parent_ref: str, object_ref: str, data):
        return object_ref

    @classmethod
    def handle_related_object(cls, parent_ref, related_object_ref, object_label, parent_has_many=False):
        cls.create_relation_to_parent(parent_ref, related_object_ref, parent_has_many)

    @classmethod
    def create_relation_to_parent(cls, parent_ref, related_object_ref: str, parent_has_many: bool = False):
        parent_model_def = cls._get_model_def(parent_ref)
        related_model_def = cls._get_model_def(related_object_ref)
        SpecificRelationFieldDef = cls._get_specific_relation_field_def(parent_has_many)
        relation_def, created = SpecificRelationFieldDef.objects.get_or_create(
            model_def=related_model_def,
            name=parent_ref,
            to=parent_model_def,
            null=True,
            blank=True
        )
        return relation_def

    @classmethod
    def _get_model_def(cls, object_name: str):
        try:
            return ModelDefinition.objects.get(object_name=object_name)
        except MultipleObjectsReturned as e:
            logger.warning(f"multiple objects found with object name {object_name}")
            return ModelDefinition.objects.filter(object_name=object_name).first()

    @classmethod
    def _get_specific_field_def(cls, value):
        return cls.ATTRIBUTE_TYPES.get(type(value))

    @classmethod
    def _get_specific_relation_field_def(cls, parent_has_many):
        return cls.RELATION_TYPES[parent_has_many]

    @classmethod
    def delete_attribute_defs(cls, model_def):
        for field_def in cls.ATTRIBUTE_TYPES.values():
            field_def.objects.filter(model_def=model_def).delete()

    @classmethod
    def delete_relation_defs(cls, model_def):
        for relation_def in cls.RELATION_TYPES.values():
            relation_def.objects.filter(model_def=model_def).delete()
            relation_def.objects.filter(to=model_def).delete()

    @classmethod
    def register_all_models(cls):
        model_defs = ModelDefinition.objects.filter(app_label=cls.APP_LABEL)
        for model_def in model_defs:
            try:
                cls.register_model_in_admin(model_def)
            except admin.sites.AlreadyRegistered:
                pass
        cls.reload_and_clear_cache_admin()

    @classmethod
    def register_model_in_admin(cls, model_def):
        ObjectModel = model_def.model_class()
        attrs = {'model': ObjectModel}
        ObjectModelAdmin = type(f'{ObjectModel.__name__}Admin', (admin.ModelAdmin,), attrs)
        admin.site.register(ObjectModel, ObjectModelAdmin)

    @classmethod
    def try_unregister_model_in_admin(cls, model_def):
        ObjectModel = model_def.model_class()
        try:
            admin.site.unregister(ObjectModel)
            cls.reload_and_clear_cache_admin()
        except NotRegistered:
            logger.warning(f"model_def: {model_def.name}, was not registered in admin.site, "
                           f"and could therefore not unregister")

    @classmethod
    def reload_and_clear_cache_admin(cls):
        reload(import_module(settings.ROOT_URLCONF))
        clear_url_caches()

