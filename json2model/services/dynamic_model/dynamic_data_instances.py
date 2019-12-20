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
        root_instance = cls.start_iterating_data_structure(data, root_label)
        return root_instance

    @classmethod
    @abstractmethod
    def handle_attribute(cls, object_ref: Model, attribute_label: str, data):
        try:
            setattr(object_ref, attribute_label, data)
        except Exception as e:
            logger.warning(f"attribute label did not exist: {e}")

    @classmethod
    @abstractmethod
    def pre_handle_object(cls, parent_ref: Model, object_label: str, data):
        DjangoModel = get_dynamic_model(model_name=object_label)
        instance = DjangoModel()
        return instance

    @classmethod
    @abstractmethod
    def post_handle_object(cls, parent_ref: str, object_ref: Model, data):
        object_ref.save()
        return object_ref

    @classmethod
    @abstractmethod
    def handle_related_object(cls, parent_ref: Model, related_object_ref: Model, object_label,
                              parent_has_many: bool = False):
        parent_label = parent_ref.__class__.__name__
        try:
            # TODO something strange is going on since i cant set the instance. but the primary key seems
            #  to work, but not very nice
            setattr(related_object_ref, f"{parent_label}_id", parent_ref)
            related_object_ref.save()
        except Exception as e:
            logger.warning(f"could not set relation between objects {parent_label} and {object_label}. {e}")
