import logging
from abc import ABC

from django.conf import settings
from django.db import IntegrityError
from mutant.contrib.numeric.models import IntegerFieldDefinition
from mutant.contrib.related.models import OneToOneFieldDefinition, ForeignKeyDefinition
from mutant.models import ModelDefinition

import json2model.services.dynamic_model.dynamic_model_admin_handler as admin_handler
from json2model.services.dynamic_model import dynamic_model_utils as dm_utils
from json2model.services.dynamic_model.attribute_types import ATTRIBUTE_TYPES
from json2model.services.dynamic_model.failed_object import FailedObject
from json2model.services.dynamic_model.i_json_iterator import IJsonIterator
from json2model.utils import handle_errors

logger = logging.getLogger(__name__)

APP_LABEL = getattr(settings, 'APP_LABEL_DYNAMIC_MODELS', "json2model")
RELATE_TO_USER = getattr(settings, 'RELATE_TO_USER', False)

RELATION_TYPES = {
    False: OneToOneFieldDefinition,
    True: ForeignKeyDefinition
}


# TODO this is related to another todo about fixing the dynamic foreign key to non dynamic models
# def get_or_create_user_model_def():
#     model_def, created = ModelDefinition.objects.get_or_create(
#         app_label='test_app',
#         object_name='abstractDummy',
#         defaults={
#             'managed': False,
#         },
#
#     )
#     return model_def
#
# def create_user_model_def():
#     model_def = ModelDefinition.objects.create(
#         app_label='test_app',
#         object_name='Dummy',
#         managed=False
#     )
#     return model_def


class DynamicModelBuilder(IJsonIterator, ABC):
    def __init__(self):
        super().__init__()

    def create_models_from_data(self, data, root_label=None):
        self.start_iterating_data_structure(data, root_label)
        admin_handler.register_all_models()

    def delete_all_dynamic_models(self, **filter_kwargs):
        model_defs = ModelDefinition.objects.filter(**filter_kwargs)
        [self._delete_dynamic_model(model_def) for model_def in model_defs]

    def delete_dynamic_model(self, model_name: str):
        model_def = dm_utils.get_model_def(model_name)
        self._delete_dynamic_model(model_def)

    def _delete_dynamic_model(self, model_def):
        admin_handler.try_unregister_model_in_admin(model_def)
        self.delete_attribute_defs(model_def)
        self.delete_relation_defs(model_def)
        model_def.delete()
        return model_def

    @handle_errors(raise_types=(IntegrityError,))
    def handle_attribute(self, object_ref, attribute_label, data):
        attribute_label, data = dm_utils.pre_handle_atts_if_list_and_specific_labels(attribute_label, data)
        field_schema = self._get_or_create_attribute(object_ref, attribute_label, data)
        return field_schema

    def _get_or_create_attribute(self, object_ref, attribute_label, data):
        SpecificFieldDefinition = self._get_specific_field_def(data)
        model_def = dm_utils.get_model_def(object_ref)
        field_schema, created = SpecificFieldDefinition.objects.get_or_create(
            name=attribute_label,
            model_def=model_def,
            blank=True,
            null=True
        )
        return field_schema

    @handle_errors()
    def pre_handle_object(self, parent_ref, object_label, data):
        try:
            model_def, created = ModelDefinition.objects.get_or_create(
                app_label=APP_LABEL,
                object_name=object_label,
                defaults={'fields': []}  # this does not work in django >=2.2.8
            )
        except IntegrityError as e:
            raise e
        except Exception as e:
            logger.error(f"object {object_label} could not be created. ERROR msg: {e}")
        else:
            return object_label

    @handle_errors()
    def post_handle_object(self, parent_ref: str, object_ref: str, data):
        if RELATE_TO_USER:
            self.create_user_ref_field(object_ref)
        return object_ref

    def create_user_ref_field(self, object_ref):
        logger.debug("creating field for user ref")
        # TODO: this is not nice, should have been foreign key instead
        # user_model_def = get_or_create_user_model_def()
        model_def = dm_utils.get_model_def(object_ref)
        user_field_def, created = IntegerFieldDefinition.objects.get_or_create(
            model_def=model_def,
            name="user_pk",
            null=True,
            blank=True
        )

    @handle_errors()
    def handle_related_object(self, parent_ref, related_object_ref, object_label, parent_has_many=False):
        if isinstance(related_object_ref, FailedObject):
            return
        else:
            self.try_get_or_create_relation_to_parent(parent_ref, related_object_ref, parent_has_many)

    def try_get_or_create_relation_to_parent(self, parent_ref, related_object_ref: str, parent_has_many: bool = False):
        parent_model_def = dm_utils.get_model_def(parent_ref)
        related_model_def = dm_utils.get_model_def(related_object_ref)
        SpecificRelationFieldDef = self._get_specific_relation_field_def(parent_has_many)
        try:
            relation_def, created = SpecificRelationFieldDef.objects.get_or_create(
                model_def=related_model_def,
                name=parent_ref,
                to=parent_model_def,
                null=True,
                blank=True
            )
        except Exception as e:
            logger.error(f"object ref {related_object_ref} could not be created. ERROR msg: {e}")
        else:
            return relation_def

    def _get_specific_field_def(self, value):
        return ATTRIBUTE_TYPES.get(type(value), ATTRIBUTE_TYPES[str])

    def _get_specific_relation_field_def(self, parent_has_many):
        return RELATION_TYPES[parent_has_many]

    def delete_attribute_defs(self, model_def):
        for field_def in ATTRIBUTE_TYPES.values():
            field_def.objects.filter(model_def=model_def).delete()

    def delete_relation_defs(self, model_def):
        for relation_def in RELATION_TYPES.values():
            relation_def.objects.filter(model_def=model_def).delete()
            relation_def.objects.filter(to=model_def).delete()
