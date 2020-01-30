import logging

from django.core.exceptions import MultipleObjectsReturned
from mutant.models import ModelDefinition

logger = logging.getLogger(__name__)

NOT_ALLOWED_ATTRIBUTE_NAMES = ("id",)


def get_dynamic_model(model_name):
    return get_model_def(model_name).model_class()


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
        return f"RENAMED__{attribute_label}"
    else:
        return attribute_label
