import logging
from abc import ABC, abstractmethod

from django.db.models.base import Model

from json2model.services.dynamic_model.dynamic_model_mutant import get_dynamic_model
from json2model.services.dynamic_model.i_json_iterator import IJsonIterator

logger = logging.getLogger(__name__)


def create_instances_from_json(root_name, data):
    return DynamicDataInstances.create_instances_from_data(root_name, data)


class DynamicDataInstances(IJsonIterator, ABC):

    @classmethod
    def create_instances_from_data(cls, root_label, data):
        root_instance = cls._iterate_data_structure(data, object_label=root_label)
        return root_instance

    @classmethod
    @abstractmethod
    def handle_attribute(cls, object_ref: Model, label: str, data):
        try:
            setattr(object_ref, label, data)
        except Exception as e:
            logger.warning(f"attribute label did not exist: {e}")

    @classmethod
    @abstractmethod
    def pre_handle_object(cls, parent_ref: Model, object_label: str, data):
        DjangoModel = get_dynamic_model(model_name=object_label)
        return DjangoModel()

    @classmethod
    @abstractmethod
    def post_handle_object(cls, parent_ref: str, object_ref: Model, data):
        object_ref.save()
        return object_ref

    @classmethod
    @abstractmethod
    def handle_related_object(cls, parent_ref: Model, related_object_ref: Model, object_label,
                              parent_has_many: bool = False):
        parent_name = parent_ref.__class__.__name__
        try:
            setattr(related_object_ref, parent_name, parent_ref)
            related_object_ref.save()
        except Exception as e:
            logger.warning(f"could not set related object: {e}")
