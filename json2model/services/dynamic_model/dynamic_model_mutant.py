import datetime
from abc import ABC

import mutant.contrib.boolean.models
import mutant.contrib.file.models
import mutant.contrib.numeric.models
import mutant.contrib.related.models
import mutant.contrib.temporal.models
import mutant.contrib.text.models
from django.contrib.sessions.backends import file
from django.utils import deprecation
from mutant.models import ModelDefinition

from json2model.services.dynamic_model.i_json_iterator import IJsonIterator


class DynamicModelMutant(IJsonIterator, ABC):
    FIELD_TYPES = {
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

    APP_LABEL = "json2model"

    @classmethod
    def create_models_from_data(cls, root_name, data):
        object_name = cls._iterate_data_structure(root_name, data)
        return cls.get_dynamic_model(object_name)

    @classmethod
    def get_dynamic_model(cls, model_name):
        return cls._get_model_def(model_name).model_class()._default_manager.model

    @classmethod
    def handle_attribute(cls, parent_name, label, data):
        model_def = cls._get_model_def(parent_name)
        SpecificFieldDefinition = cls._get_specific_field_def(data)
        field_schema = SpecificFieldDefinition.objects.get_or_create(
            name=label,
            model_def=model_def
        )
        return field_schema

    @classmethod
    def handle_attribute_lists(cls, parent_name, label, value):
        raise NotImplementedError

    @classmethod
    def handle_object(cls, parent_object, label, data):
        model_def, created = ModelDefinition.objects.get_or_create(
            app_label=cls.APP_LABEL,
            object_name=label,
            defaults={'fields': []},  # [CharFieldDefinition(name='char_field', max_length=25)]}
        )
        return model_def

    @classmethod
    def handle_related_object(cls, parent_label, label, data):
        related_object = cls._iterate_data_structure(label, data)
        cls.create_relation_to_parent(parent_label, label, data)
        return related_object

    @classmethod
    def create_relation_to_parent(cls, parent_label, label, data):
        model_def = cls._get_model_def(parent_label)
        related_model_def = cls._get_model_def(label)
        SpecificRelationFieldDef = cls._get_specific_relation_field_def(data)
        SpecificRelationFieldDef.objects.create(model_def=model_def, name=label, to=related_model_def)

    @classmethod
    def _get_model_def(cls, object_name):
        return ModelDefinition.objects.get(object_name=object_name)

    @classmethod
    def _create_or_get_model_def(cls, object_name):
        model_def, created = ModelDefinition.objects.get_or_create(
            app_label=cls.APP_LABEL,
            object_name=object_name,
            defaults={'fields': []},  # [CharFieldDefinition(name='char_field', max_length=25)]}
        )
        return model_def

    @classmethod
    def _create_object_instance(cls, model_def, related_instances: dict, properties: dict):
        Model = model_def.model_class()
        if isinstance(related_instances, list):
            pass
        return Model.objects.create(**properties, **related_instances)

    @classmethod
    def _get_specific_field_def(cls, value):
        return cls.FIELD_TYPES.get(type(value))

    @classmethod
    def _get_specific_relation_field_def(cls, value):
        if isinstance(value, dict):
            return mutant.contrib.related.models.ForeignKeyDefinition
        elif isinstance(value, list):
            return mutant.contrib.related.models.ForeignKeyDefinition


