import logging

from django.core.exceptions import MultipleObjectsReturned
from mutant.models import ModelDefinition

from json2model.services.dynamic_model.attribute_types import ATTRIBUTE_TYPES

logger = logging.getLogger(__name__)

NOT_ALLOWED_ATTRIBUTE_NAMES = ("id",)


def get_dynamic_model(model_name):
    try:
        return get_model_def(model_name).model_class()
    except ModelDefinition.DoesNotExist as e:
        e.args = (f"{e.args[0]} Could not find model with name: {model_name}",)
        raise e


def get_dynamic_attribute(attribute_name: str, object_name: str = None):
    found_attributes = []
    for AttrClass in ATTRIBUTE_TYPES.values():
        att = AttrClass.objects.filter(name=attribute_name, object_name=object_name)
        found_attributes.extend(att)
    if len(found_attributes) > 1:
        logger.warning(f"get_dynamic_attribute found more than one with name {attribute_name} \
                        and object name {object_name}")
    return None or next(found_attributes)


def get_model_def(object_name: str):
    try:
        return ModelDefinition.objects.get(object_name=object_name)
    except MultipleObjectsReturned as e:
        logger.warning(f"multiple objects found with object name {object_name}")
        return ModelDefinition.objects.filter(object_name=object_name).first()


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
