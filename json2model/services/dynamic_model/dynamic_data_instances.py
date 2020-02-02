import logging
from abc import ABC

from django.conf import settings
from django.db.models.base import Model

from json2model.services.dynamic_model import dynamic_model_utils as dm_utils
from json2model.services.dynamic_model.i_json_iterator import IJsonIterator

logger = logging.getLogger(__name__)

RELATE_TO_USER = getattr(settings, 'RELATE_TO_USER', False)


class DynamicDataInstances(IJsonIterator, ABC):
    def __init__(self, user_pk=None):
        super().__init__()
        self.user_pk = user_pk

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
        if RELATE_TO_USER:
            self.relate_object_to_user(object_ref)
        object_ref.save()
        return object_ref

    def relate_object_to_user(self, object_ref: Model):
        logger.debug(f"attaching user id {self.user_pk} to model {object_ref}")
        object_ref.user_pk = self.user_pk

    def handle_related_object(self, parent_ref: Model, related_object_ref: Model, object_label,
                              parent_has_many: bool = False):
        parent_label = parent_ref.__class__.__name__
        try:
            self.try_set_related_object(parent_label, parent_ref, related_object_ref)
        except Exception as e:
            logger.warning(f"could not set relation between objects {parent_label} and {object_label}. {e}")

    def try_set_related_object(self, parent_label, parent_ref, related_object_ref):
        # TODO something strange is going on since i cant set the instance. but the primary key seems
        #  to work, but not very nice. should have been this, if it does not work try the other.
        try:
            setattr(related_object_ref, parent_label, parent_ref)
        except:
            logger.warning("could not relate objects by obj_ref, trying with pk instead")
            setattr(related_object_ref, f"{parent_label}_id", parent_ref.pk)
        finally:
            related_object_ref.save()
