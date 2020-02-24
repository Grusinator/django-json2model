import logging

from django.core.exceptions import MultipleObjectsReturned
from mutant.models import ModelDefinition

from json2model.services.dynamic_model.attribute_types import ATTRIBUTE_TYPES

logger = logging.getLogger(__name__)

NOT_ALLOWED_ATTRIBUTE_NAMES = ("id",)


def get_dynamic_model(model_name, prefix=None):
    return get_model_def(model_name, prefix).model_class()


def is_already_prefixed(object_label, prefix):
    return prefix == object_label[:len(prefix)]


def add_prefix_to_model_label(object_label, prefix):
    if prefix and not is_already_prefixed(object_label, prefix):
        object_label = f"{prefix}_{object_label}"
    return object_label


def get_dynamic_attribute(attribute_name: str, object_name: str = None):
    found_attributes = []
    filter_args = {"name": attribute_name}
    if object_name:
        filter_args["model_def__object_name"] = object_name
    for AttrClass in ATTRIBUTE_TYPES.values():
        att = AttrClass.objects.filter(**filter_args)
        found_attributes.extend(att)
    if len(found_attributes) > 1:
        logger.warning(f"get_dynamic_attribute found more than one with name {attribute_name} \
                        and object name {object_name}")
    return next(iter(found_attributes), None)


def get_model_def(object_name: str, prefix=None):
    search_args = build_search_kwargs(object_name, prefix)
    try:
        return ModelDefinition.objects.get(**search_args)
    except ModelDefinition.DoesNotExist as e:
        e.args = (f"{e.args[0]} Could not find model with name: {object_name}",)
        raise e
    except MultipleObjectsReturned as e:
        logger.warning(f"multiple objects found with object name {object_name}")
        return ModelDefinition.objects.filter(**search_args).first()


def build_search_kwargs(object_name, prefix):
    search_key = "object_name"
    if prefix:
        object_name = add_prefix_to_model_label(object_name, prefix)
    else:
        search_key += "__endswith"
    search_args = {search_key: object_name}
    return search_args


def pre_handle_atts_if_list_and_specific_labels(attribute_label, data):
    if not attribute_label:
        raise Exception("something is wrong here")
    data = handle_attribute_lists(data)
    attribute_label = handle_specific_attribute_labels(attribute_label)
    return attribute_label, data


def handle_attribute_lists(data):
    if isinstance(data, list):
        # TODO this should be done better
        data = str(data)
    return data


def handle_specific_attribute_labels(attribute_label):
    if attribute_label in NOT_ALLOWED_ATTRIBUTE_NAMES:
        return f"EXTERNAL_RENAMED_{attribute_label}"
    else:
        return attribute_label


def get_all_dynamic_models(filter: dict = None):
    if filter is None:
        filter = {}
    return [model_def.model_class() for model_def in ModelDefinition.objects.filter(**filter)]


def get_all_model_definition_names():
    return [model_def.object_name for model_def in ModelDefinition.objects.all()]
