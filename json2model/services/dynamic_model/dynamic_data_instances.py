import logging
from abc import ABC

from django.db.models.base import Model

from json2model.services.dynamic_model import dynamic_model_utils as dm_utils
from json2model.services.dynamic_model.i_json_iterator import IJsonIterator

logger = logging.getLogger(__name__)


class DynamicDataInstances(IJsonIterator, ABC):
    def __init__(self):
        super().__init__()

    def create_instances_from_data(self, root_label, data):
        root_instance = self.start_iterating_data_structure(data, root_label)
        return root_instance

    def handle_attribute(self, object_ref: Model, attribute_label: str, data):
        attribute_label, data = dm_utils.pre_handle_atts_if_list_and_specific_labels(attribute_label, data)
        self.try_set_attribute(attribute_label, data, object_ref)

    def try_set_attribute(self, attribute_label, data, object_ref):
        try:
            setattr(object_ref, attribute_label, data)
        except Exception as e:
            logger.warning(f"attribute label did not exist: {e}")

    def pre_handle_object(self, parent_ref: Model, object_label: str, data):
        DjangoModel = dm_utils.get_dynamic_model(model_name=object_label)
        instance = DjangoModel()
        return instance

    def post_handle_object(self, parent_ref: str, object_ref: Model, data):
        object_ref.save()
        return object_ref

    def handle_related_object(self, parent_ref: Model, related_object_ref: Model, object_label,
                              parent_has_many: bool = False):
        parent_label = parent_ref.__class__.__name__
        try:
            # TODO something strange is going on since i cant set the instance. but the primary key seems
            #  to work, but not very nice
            setattr(related_object_ref, f"{parent_label}_id", parent_ref)
            related_object_ref.save()
        except Exception as e:
            logger.warning(f"could not set relation between objects {parent_label} and {object_label}. {e}")
